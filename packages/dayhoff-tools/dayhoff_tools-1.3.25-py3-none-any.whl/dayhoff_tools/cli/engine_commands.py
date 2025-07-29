"""Engine and Studio management commands for DHT CLI."""

import json
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import boto3
import requests
import typer
from botocore.exceptions import ClientError, NoCredentialsError
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table
import re

# Initialize Typer apps
engine_app = typer.Typer(help="Manage compute engines for development.")
studio_app = typer.Typer(help="Manage persistent development studios.")

console = Console()

# Cost information
HOURLY_COSTS = {
    "cpu": 0.50,  # r6i.2xlarge
    "cpumax": 2.02,  # r7i.8xlarge
    "t4": 0.75,  # g4dn.2xlarge
    "a10g": 1.50,  # g5.2xlarge
    "a100": 21.96,  # p4d.24xlarge
}

# SSH config management
SSH_MANAGED_COMMENT = "# Managed by dh engine"

# --------------------------------------------------------------------------------
# Bootstrap stage helpers
# --------------------------------------------------------------------------------

def _colour_stage(stage: str) -> str:
    """Return colourised stage name for table output."""
    if not stage:
        return "[dim]-[/dim]"
    low = stage.lower()
    if low.startswith("error"):
        return f"[red]{stage}[/red]"
    if low == "finished":
        return f"[green]{stage}[/green]"
    return f"[yellow]{stage}[/yellow]"


def _fetch_init_stages(instance_ids: List[str]) -> Dict[str, str]:
    """Fetch DayhoffInitStage tag for many instances in one call."""
    if not instance_ids:
        return {}
    ec2 = boto3.client("ec2", region_name="us-east-1")
    stages: Dict[str, str] = {}
    try:
        paginator = ec2.get_paginator("describe_instances")
        for page in paginator.paginate(InstanceIds=instance_ids):
            for res in page["Reservations"]:
                for inst in res["Instances"]:
                    iid = inst["InstanceId"]
                    tag_val = next((t["Value"] for t in inst.get("Tags", []) if t["Key"] == "DayhoffInitStage"), None)
                    if tag_val:
                        stages[iid] = tag_val
    except Exception:
        pass  # best-effort
    return stages


def check_aws_sso() -> str:
    """Check AWS SSO status and return username."""
    try:
        sts = boto3.client("sts")
        identity = sts.get_caller_identity()
        # Parse username from assumed role ARN
        # Format: arn:aws:sts::123456789012:assumed-role/AWSReservedSSO_DeveloperAccess_xxxx/username
        arn = identity["Arn"]
        if "assumed-role" in arn:
            username = arn.split("/")[-1]
            return username
        else:
            # Fallback for other auth methods
            return identity["UserId"].split(":")[-1]
    except (NoCredentialsError, ClientError):
        console.print("[red]❌ Not logged in to AWS SSO[/red]")
        console.print("Please run: [cyan]aws sso login[/cyan]")
        if Confirm.ask("Would you like to login now?"):
            try:
                result = subprocess.run(
                    ["aws", "sso", "login"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                if result.returncode == 0:
                    console.print("[green]✓ Successfully logged in![/green]")
                    return check_aws_sso()
            except subprocess.CalledProcessError as e:
                console.print(f"[red]Login failed: {e}[/red]")
        raise typer.Exit(1)


def get_api_url() -> str:
    """Get Studio Manager API URL from SSM Parameter Store."""
    ssm = boto3.client("ssm", region_name="us-east-1")
    try:
        response = ssm.get_parameter(Name="/dev/studio-manager/api-url")
        return response["Parameter"]["Value"]
    except ClientError as e:
        if e.response["Error"]["Code"] == "ParameterNotFound":
            console.print(
                "[red]❌ API URL parameter not found in SSM Parameter Store[/red]"
            )
            console.print(
                "Please ensure the Studio Manager infrastructure is deployed."
            )
        else:
            console.print(f"[red]❌ Error retrieving API URL: {e}[/red]")
        raise typer.Exit(1)


def make_api_request(
    method: str,
    endpoint: str,
    json_data: Optional[Dict] = None,
    params: Optional[Dict] = None,
) -> requests.Response:
    """Make an API request with error handling."""
    api_url = get_api_url()
    url = f"{api_url}{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=json_data)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        return response
    except requests.exceptions.RequestException as e:
        console.print(f"[red]❌ API request failed: {e}[/red]")
        raise typer.Exit(1)


def format_duration(duration: timedelta) -> str:
    """Format a duration as a human-readable string."""
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"


def get_disk_usage_via_ssm(instance_id: str) -> Optional[str]:
    """Get disk usage for an engine via SSM.
    
    Returns:
        String like "17/50 GB" or None if failed
    """
    try:
        ssm = boto3.client("ssm", region_name="us-east-1")
        
        # Run df command to get disk usage
        response = ssm.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={
                "commands": [
                    # Get root filesystem usage in GB
                    "df -BG / | tail -1 | awk '{gsub(/G/, \"\", $2); gsub(/G/, \"\", $3); print $3 \"/\" $2 \" GB\"}'"
                ],
                "executionTimeout": ["10"],
            },
        )
        
        command_id = response["Command"]["CommandId"]
        
        # Wait for command to complete (with timeout)
        for _ in range(5):  # 5 second timeout
            time.sleep(1)
            result = ssm.get_command_invocation(
                CommandId=command_id,
                InstanceId=instance_id,
            )
            if result["Status"] in ["Success", "Failed"]:
                break
        
        if result["Status"] == "Success":
            output = result["StandardOutputContent"].strip()
            return output if output else None
        
        return None
        
    except Exception as e:
        # logger.debug(f"Failed to get disk usage for {instance_id}: {e}") # Original code had this line commented out
        return None


def get_studio_disk_usage_via_ssm(instance_id: str, username: str) -> Optional[str]:
    """Get disk usage for a studio via SSM.
    
    Returns:
        String like "333/500 GB" or None if failed
    """
    try:
        ssm = boto3.client("ssm", region_name="us-east-1")
        
        # Run df command to get studio disk usage
        response = ssm.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={
                "commands": [
                    # Get studio filesystem usage in GB
                    f"df -BG /studios/{username} 2>/dev/null | tail -1 | awk '{{gsub(/G/, \"\", $2); gsub(/G/, \"\", $3); print $3 \"/\" $2 \" GB\"}}'"
                ],
                "executionTimeout": ["10"],
            },
        )
        
        command_id = response["Command"]["CommandId"]
        
        # Wait for command to complete (with timeout)
        for _ in range(5):  # 5 second timeout
            time.sleep(1)
            result = ssm.get_command_invocation(
                CommandId=command_id,
                InstanceId=instance_id,
            )
            if result["Status"] in ["Success", "Failed"]:
                break
        
        if result["Status"] == "Success":
            output = result["StandardOutputContent"].strip()
            return output if output else None
        
        return None
        
    except Exception:
        return None


def parse_launch_time(launch_time_str: str) -> datetime:
    """Parse launch time from API response."""
    # Try different datetime formats
    formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",  # ISO format with timezone
        "%Y-%m-%dT%H:%M:%S+00:00",  # Explicit UTC offset
        "%Y-%m-%d %H:%M:%S",
    ]

    # First try parsing with fromisoformat for better timezone handling
    try:
        # Handle the ISO format properly
        return datetime.fromisoformat(launch_time_str.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        pass

    # Fallback to manual format parsing
    for fmt in formats:
        try:
            parsed = datetime.strptime(launch_time_str, fmt)
            # If no timezone info, assume UTC
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed
        except ValueError:
            continue

    # Fallback: assume it's recent
    return datetime.now(timezone.utc)


def format_status(state: str, ready: Optional[bool]) -> str:
    """Format engine status with ready indicator."""
    if state.lower() == "running":
        if ready is True:
            return "[green]Running ✓[/green]"
        elif ready is False:
            return "[yellow]Running ⚠ (Bootstrapping...)[/yellow]"
        else:
            return "[green]Running[/green]"
    elif state.lower() == "stopped":
        return "[dim]Stopped[/dim]"
    elif state.lower() == "stopping":
        return "[yellow]Stopping...[/yellow]"
    elif state.lower() == "pending":
        return "[yellow]Starting...[/yellow]"
    else:
        return state


def resolve_engine(name_or_id: str, engines: List[Dict]) -> Dict:
    """Resolve engine by name or ID with interactive selection."""
    # Exact ID match
    exact_id = [e for e in engines if e["instance_id"] == name_or_id]
    if exact_id:
        return exact_id[0]

    # Exact name match
    exact_name = [e for e in engines if e["name"] == name_or_id]
    if len(exact_name) == 1:
        return exact_name[0]

    # Prefix matches
    matches = [
        e
        for e in engines
        if e["name"].startswith(name_or_id) or e["instance_id"].startswith(name_or_id)
    ]

    if len(matches) == 0:
        console.print(f"[red]❌ No engine found matching '{name_or_id}'[/red]")
        raise typer.Exit(1)
    elif len(matches) == 1:
        return matches[0]
    else:
        # Interactive selection
        console.print(f"Multiple engines match '{name_or_id}':")
        for i, engine in enumerate(matches, 1):
            cost = HOURLY_COSTS.get(engine["engine_type"], 0)
            console.print(
                f"  {i}. [cyan]{engine['name']}[/cyan] ({engine['instance_id']}) "
                f"- {engine['engine_type']} - {engine['state']} - ${cost:.2f}/hr"
            )

        while True:
            try:
                choice = IntPrompt.ask(
                    "Select engine",
                    default=1,
                    choices=[str(i) for i in range(1, len(matches) + 1)],
                )
                return matches[choice - 1]
            except (ValueError, IndexError):
                console.print("[red]Invalid selection, please try again[/red]")


def get_ssh_public_key() -> str:
    """Get the user's SSH public key."""
    home = Path.home()
    key_paths = [home / ".ssh" / "id_ed25519.pub", home / ".ssh" / "id_rsa.pub"]

    for key_path in key_paths:
        if key_path.is_file():
            return key_path.read_text().strip()

    raise FileNotFoundError(
        "No SSH public key found. Please create one with 'ssh-keygen' first."
    )


def update_ssh_config_entry(engine_name: str, instance_id: str, ssh_user: str):
    """Add or update a single SSH config entry for the given SSH user."""
    config_path = Path.home() / ".ssh" / "config"
    config_path.parent.mkdir(mode=0o700, exist_ok=True)

    # Touch the file if it doesn't exist
    if not config_path.exists():
        config_path.touch(mode=0o600)

    # Read existing config
    content = config_path.read_text()

    # Create new entry
    new_entry = f"""
Host {engine_name} {SSH_MANAGED_COMMENT}
    HostName {instance_id}
    User {ssh_user}
    ProxyCommand sh -c "aws ssm start-session --target %h --document-name AWS-StartSSHSession --parameters 'portNumber=%p'"
"""

    # Check if entry already exists
    host_line = f"Host {engine_name} {SSH_MANAGED_COMMENT}"
    if host_line in content:
        # Update existing entry
        lines = content.splitlines()
        new_lines = []
        skip_count = 0
        for line in lines:
            if line.strip() == host_line.strip():
                new_lines.extend(new_entry.strip().splitlines())
                skip_count = 4  # Skip the next 4 lines (old entry)
            elif skip_count > 0:
                skip_count -= 1
                continue
            else:
                new_lines.append(line)
        content = "\n".join(new_lines)
    else:
        # Append new entry
        content = content.rstrip() + "\n" + new_entry

    # Write back
    config_path.write_text(content)
    config_path.chmod(0o600)


# ==================== ENGINE COMMANDS ====================


@engine_app.command("launch")
def launch_engine(
    name: str = typer.Argument(help="Name for the new engine"),
    engine_type: str = typer.Option(
        "cpu",
        "--type",
        "-t",
        help="Engine type: cpu, cpumax, t4, a10g, a100",
    ),
    user: Optional[str] = typer.Option(None, "--user", "-u", help="Override username"),
    boot_disk_size: Optional[int] = typer.Option(
        None,
        "--size",
        "-s",
        help="Boot disk size in GB (default: 50GB, min: 20GB, max: 1000GB)",
    ),
):
    """Launch a new engine instance."""
    username = check_aws_sso()
    if user:
        username = user

    # Validate engine type
    valid_types = ["cpu", "cpumax", "t4", "a10g", "a100"]
    if engine_type not in valid_types:
        console.print(f"[red]❌ Invalid engine type: {engine_type}[/red]")
        console.print(f"Valid types: {', '.join(valid_types)}")
        raise typer.Exit(1)

    # Validate boot disk size
    if boot_disk_size is not None:
        if boot_disk_size < 20:
            console.print("[red]❌ Boot disk size must be at least 20GB[/red]")
            raise typer.Exit(1)
        if boot_disk_size > 1000:
            console.print("[red]❌ Boot disk size cannot exceed 1000GB[/red]")
            raise typer.Exit(1)

    cost = HOURLY_COSTS.get(engine_type, 0)
    disk_info = f" with {boot_disk_size}GB boot disk" if boot_disk_size else ""
    console.print(
        f"Launching [cyan]{name}[/cyan] ({engine_type}){disk_info} for ${cost:.2f}/hour..."
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("Creating engine...", total=None)

        request_data = {
            "name": name,
            "user": username,
            "engine_type": engine_type,
        }
        if boot_disk_size is not None:
            request_data["boot_disk_size"] = boot_disk_size

        response = make_api_request("POST", "/engines", json_data=request_data)

    if response.status_code == 201:
        data = response.json()
        console.print(f"[green]✓ Engine launched successfully![/green]")
        console.print(f"Instance ID: [cyan]{data['instance_id']}[/cyan]")
        console.print(f"Type: {data['instance_type']} (${cost:.2f}/hour)")
        if boot_disk_size:
            console.print(f"Boot disk: {boot_disk_size}GB")
        console.print("\nThe engine is initializing. This may take a few minutes.")
        console.print(f"Check status with: [cyan]dh engine status {name}[/cyan]")
    else:
        error = response.json().get("error", "Unknown error")
        console.print(f"[red]❌ Failed to launch engine: {error}[/red]")


@engine_app.command("list")
def list_engines(
    user: Optional[str] = typer.Option(None, "--user", "-u", help="Filter by user"),
    running_only: bool = typer.Option(
        False, "--running", help="Show only running engines"
    ),
    stopped_only: bool = typer.Option(
        False, "--stopped", help="Show only stopped engines"
    ),
):
    """List engines (shows all engines by default)."""
    current_user = check_aws_sso()

    params = {}
    if user:
        params["user"] = user

    response = make_api_request("GET", "/engines", params=params)

    if response.status_code == 200:
        data = response.json()
        engines = data.get("engines", [])

        # Filter by state if requested
        if running_only:
            engines = [e for e in engines if e["state"].lower() == "running"]
        elif stopped_only:
            engines = [e for e in engines if e["state"].lower() == "stopped"]

        if not engines:
            console.print("No engines found.")
            return

        # Fetch bootstrap stages once
        stages_map = _fetch_init_stages([e["instance_id"] for e in engines])

        # Create table
        table = Table(title="Engines", box=box.ROUNDED)
        table.add_column("Name", style="cyan")
        table.add_column("Instance ID", style="dim")
        table.add_column("Type")
        table.add_column("User")
        table.add_column("Status")
        table.add_column("Disk Usage")
        table.add_column("Uptime/Since")
        table.add_column("$/hour", justify="right")
        table.add_column("Cost Today", justify="right", style="yellow")

        total_cost = 0.0
        for engine in engines:
            launch_time = parse_launch_time(engine["launch_time"])
            uptime = datetime.now(timezone.utc) - launch_time
            hourly_cost = HOURLY_COSTS.get(engine["engine_type"], 0)

            if engine["state"].lower() == "running":
                daily_cost = hourly_cost * min(uptime.total_seconds() / 3600, 24)
                total_cost += daily_cost
                time_str = format_duration(uptime)
                # Get disk usage for running engines
                disk_usage = get_disk_usage_via_ssm(engine["instance_id"]) or "-"
            else:
                daily_cost = 0
                time_str = launch_time.strftime("%Y-%m-%d %H:%M")
                disk_usage = "-"

            table.add_row(
                engine["name"],
                engine["instance_id"],
                engine["engine_type"],
                engine["user"],
                format_status(engine["state"], engine.get("ready")),
                disk_usage,
                time_str,
                f"${hourly_cost:.2f}",
                f"${daily_cost:.2f}" if daily_cost > 0 else "-",
            )

        console.print(table)

        if total_cost > 0:
            console.print(f"\n[yellow]Total cost today: ${total_cost:.2f}[/yellow]")
    else:
        error = response.json().get("error", "Unknown error")
        console.print(f"[red]❌ Failed to list engines: {error}[/red]")


@engine_app.command("status")
def engine_status(
    name_or_id: str = typer.Argument(help="Engine name or instance ID"),
    show_log: bool = typer.Option(False, "--show-log", help="Show bootstrap log"),
):
    """Show detailed engine status and information."""
    check_aws_sso()

    # Get all engines to resolve name
    response = make_api_request("GET", "/engines")
    if response.status_code != 200:
        console.print("[red]❌ Failed to fetch engines[/red]")
        raise typer.Exit(1)

    engines = response.json().get("engines", [])
    engine = resolve_engine(name_or_id, engines)

    # Get attached studios info
    response = make_api_request(
        "GET", f"/engines/{engine['instance_id']}/attached-studios"
    )
    attached_studios = []
    if response.status_code == 200:
        attached_studios = response.json().get("studios", [])

    # Calculate costs
    launch_time = parse_launch_time(engine["launch_time"])
    uptime = datetime.now(timezone.utc) - launch_time
    hourly_cost = HOURLY_COSTS.get(engine["engine_type"], 0)
    total_cost = hourly_cost * (uptime.total_seconds() / 3600)

    stages_map = _fetch_init_stages([engine["instance_id"]])
    stage_val = stages_map.get(engine["instance_id"], "-")

    status_lines = [
        f"[bold]Name:[/bold]        {engine['name']}",
        f"[bold]Instance:[/bold]    {engine['instance_id']}",
        f"[bold]Type:[/bold]        {engine['engine_type']} ({engine['instance_type']})",
        f"[bold]Status:[/bold]      {format_status(engine['state'], engine.get('ready'))}",
        f"[bold]Bootstrap:[/bold]   {_colour_stage(stage_val)}",
        f"[bold]User:[/bold]        {engine['user']}",
        f"[bold]IP:[/bold]          {engine.get('public_ip', 'N/A')}",
        f"[bold]Launched:[/bold]    {launch_time.strftime('%Y-%m-%d %H:%M:%S')} ({format_duration(uptime)} ago)",
        f"[bold]Cost:[/bold]        ${hourly_cost:.2f}/hour (${total_cost:.2f} total)",
    ]

    # Health report (only if bootstrap finished)
    if stage_val == "finished":
        try:
            ssm = boto3.client("ssm", region_name="us-east-1")
            res = ssm.send_command(
                InstanceIds=[engine["instance_id"]],
                DocumentName="AWS-RunShellScript",
                Parameters={"commands": ["cat /opt/dayhoff/state/engine-health.json 2>/dev/null || cat /var/run/engine-health.json 2>/dev/null || true"], "executionTimeout": ["10"]},
            )
            cid = res["Command"]["CommandId"]
            time.sleep(1)
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=engine["instance_id"])
            if inv["Status"] == "Success":
                import json as _json
                health = _json.loads(inv["StandardOutputContent"].strip() or "{}")
                status_lines.append("")
                status_lines.append("[bold]Health:[/bold]")
                status_lines.append(f"  • GPU Drivers: {'OK' if health.get('drivers_ok') else 'MISSING'}")
                status_lines.append(f"  • Idle Detector: {health.get('idle_detector_timer', 'unknown')}")
        except Exception:
            pass

    if attached_studios:
        status_lines.append("")
        status_lines.append("[bold]Attached Studios:[/bold]")
        for studio in attached_studios:
            attach_time = studio.get("attach_time", "Unknown")
            status_lines.append(
                f"  • {studio['user']} ({studio['studio_id']}) - attached {attach_time}"
            )

    console.print(Panel("\n".join(status_lines), title="Engine Status", border_style="blue"))

    if show_log:
        console.print("\n[bold]Bootstrap Log:[/bold]")
        try:
            ssm = boto3.client("ssm", region_name="us-east-1")
            resp = ssm.send_command(
                InstanceIds=[engine["instance_id"]],
                DocumentName="AWS-RunShellScript",
                Parameters={"commands": ["cat /var/log/engine-setup.log 2>/dev/null || echo 'No setup log found'"], "executionTimeout": ["15"]},
            )
            cid = resp["Command"]["CommandId"]
            time.sleep(2)
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=engine["instance_id"])
            if inv["Status"] == "Success":
                log_content = inv["StandardOutputContent"].strip()
                if log_content:
                    console.print(f"[dim]{log_content}[/dim]")
                else:
                    console.print("[yellow]No bootstrap log available[/yellow]")
            else:
                console.print("[red]❌ Could not retrieve bootstrap log[/red]")
        except Exception as e:
            console.print(f"[red]❌ Error fetching log: {e}[/red]")


@engine_app.command("stop")
def stop_engine(
    name_or_id: str = typer.Argument(help="Engine name or instance ID"),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force stop and detach all studios"
    ),
):
    """Stop an engine."""
    check_aws_sso()

    # Get all engines to resolve name
    response = make_api_request("GET", "/engines")
    if response.status_code != 200:
        console.print("[red]❌ Failed to fetch engines[/red]")
        raise typer.Exit(1)

    engines = response.json().get("engines", [])
    engine = resolve_engine(name_or_id, engines)

    console.print(f"Stopping engine [cyan]{engine['name']}[/cyan]...")

    # First attempt without detaching
    response = make_api_request(
        "POST",
        f"/engines/{engine['instance_id']}/stop",
        json_data={"detach_studios": force},
    )

    if response.status_code == 409 and not force:
        # Engine has attached studios
        data = response.json()
        attached_studios = data.get("attached_studios", [])

        console.print("\n[yellow]⚠️  This engine has attached studios:[/yellow]")
        for studio in attached_studios:
            console.print(f"  • {studio['user']} ({studio['studio_id']})")

        if Confirm.ask("\nDetach all studios and stop the engine?"):
            response = make_api_request(
                "POST",
                f"/engines/{engine['instance_id']}/stop",
                json_data={"detach_studios": True},
            )
        else:
            console.print("Stop cancelled.")
            return

    if response.status_code == 200:
        console.print(f"[green]✓ Engine stopped successfully![/green]")
    else:
        error = response.json().get("error", "Unknown error")
        console.print(f"[red]❌ Failed to stop engine: {error}[/red]")


@engine_app.command("start")
def start_engine(
    name_or_id: str = typer.Argument(help="Engine name or instance ID"),
):
    """Start a stopped engine."""
    check_aws_sso()

    # Get all engines to resolve name
    response = make_api_request("GET", "/engines")
    if response.status_code != 200:
        console.print("[red]❌ Failed to fetch engines[/red]")
        raise typer.Exit(1)

    engines = response.json().get("engines", [])
    engine = resolve_engine(name_or_id, engines)

    console.print(f"Starting engine [cyan]{engine['name']}[/cyan]...")

    response = make_api_request("POST", f"/engines/{engine['instance_id']}/start")

    if response.status_code == 200:
        data = response.json()
        console.print(f"[green]✓ Engine started successfully![/green]")
        console.print(f"New public IP: {data.get('public_ip', 'Pending...')}")
    else:
        error = response.json().get("error", "Unknown error")
        console.print(f"[red]❌ Failed to start engine: {error}[/red]")


@engine_app.command("terminate")
def terminate_engine(
    name_or_id: str = typer.Argument(help="Engine name or instance ID"),
):
    """Permanently terminate an engine."""
    check_aws_sso()

    # Get all engines to resolve name
    response = make_api_request("GET", "/engines")
    if response.status_code != 200:
        console.print("[red]❌ Failed to fetch engines[/red]")
        raise typer.Exit(1)

    engines = response.json().get("engines", [])
    engine = resolve_engine(name_or_id, engines)

    # Calculate cost
    launch_time = parse_launch_time(engine["launch_time"])
    uptime = datetime.now(timezone.utc) - launch_time
    hourly_cost = HOURLY_COSTS.get(engine["engine_type"], 0)
    total_cost = hourly_cost * (uptime.total_seconds() / 3600)

    console.print(
        f"\n[yellow]⚠️  This will permanently terminate engine '{engine['name']}'[/yellow]"
    )
    console.print(f"Total cost for this session: ${total_cost:.2f}")

    if not Confirm.ask("\nAre you sure you want to terminate this engine?"):
        console.print("Termination cancelled.")
        return

    response = make_api_request("DELETE", f"/engines/{engine['instance_id']}")

    if response.status_code == 200:
        console.print(f"[green]✓ Engine terminated successfully![/green]")
    else:
        error = response.json().get("error", "Unknown error")
        console.print(f"[red]❌ Failed to terminate engine: {error}[/red]")


@engine_app.command("ssh")
def ssh_engine(
    name_or_id: str = typer.Argument(help="Engine name or instance ID"),
    admin: bool = typer.Option(False, "--admin", help="Connect as ec2-user instead of the engine owner user"),
):
    """Connect to an engine via SSH.

    By default the CLI connects using the engine's owner username (the same one stored in the `User` tag).
    Pass `--admin` to connect with the underlying [`ec2-user`] account for break-glass or debugging.
    """
    username = check_aws_sso()

    # Get all engines to resolve name
    response = make_api_request("GET", "/engines")
    if response.status_code != 200:
        console.print("[red]❌ Failed to fetch engines[/red]")
        raise typer.Exit(1)

    engines = response.json().get("engines", [])
    engine = resolve_engine(name_or_id, engines)

    if engine["state"].lower() != "running":
        console.print(f"[red]❌ Engine is not running (state: {engine['state']})[/red]")
        raise typer.Exit(1)

    # Choose SSH user
    ssh_user = "ec2-user" if admin else username

    # Update SSH config
    console.print(f"Updating SSH config for [cyan]{engine['name']}[/cyan] (user: {ssh_user})...")
    update_ssh_config_entry(engine["name"], engine["instance_id"], ssh_user)

    # Connect
    console.print(f"[green]✓ Connecting to {engine['name']}...[/green]")
    subprocess.run(["ssh", engine["name"]])


@engine_app.command("config-ssh")
def config_ssh(
    clean: bool = typer.Option(False, "--clean", help="Remove all managed entries"),
    all_engines: bool = typer.Option(
        False, "--all", "-a", help="Include all engines from all users"
    ),
    admin: bool = typer.Option(False, "--admin", help="Generate entries that use ec2-user instead of per-engine owner user"),
):
    """Update SSH config with available engines."""
    username = check_aws_sso()

    if clean:
        console.print("Removing all managed SSH entries...")
    else:
        if all_engines:
            console.print("Updating SSH config with all running engines...")
        else:
            console.print(
                f"Updating SSH config with running engines for [cyan]{username}[/cyan] and [cyan]shared[/cyan]..."
            )

    # Get all engines
    response = make_api_request("GET", "/engines")
    if response.status_code != 200:
        console.print("[red]❌ Failed to fetch engines[/red]")
        raise typer.Exit(1)

    engines = response.json().get("engines", [])
    running_engines = [e for e in engines if e["state"].lower() == "running"]

    # Filter engines based on options
    if not all_engines:
        # Show only current user's engines and shared engines
        running_engines = [
            e for e in running_engines if e["user"] == username or e["user"] == "shared"
        ]

    # Read existing config
    config_path = Path.home() / ".ssh" / "config"
    config_path.parent.mkdir(mode=0o700, exist_ok=True)

    if config_path.exists():
        content = config_path.read_text()
        lines = content.splitlines()
    else:
        content = ""
        lines = []

    # Remove old managed entries
    new_lines = []
    skip_until_next_host = False
    for line in lines:
        if SSH_MANAGED_COMMENT in line:
            skip_until_next_host = True
        elif line.strip().startswith("Host ") and skip_until_next_host:
            skip_until_next_host = False
            # Check if this is a managed host
            if SSH_MANAGED_COMMENT not in line:
                new_lines.append(line)
        elif not skip_until_next_host:
            new_lines.append(line)

    # Add new entries if not cleaning
    if not clean:
        for engine in running_engines:
            # Determine ssh user based on --admin flag
            ssh_user = 'ec2-user' if admin else username
            new_lines.extend(
                [
                    "",
                    f"Host {engine['name']} {SSH_MANAGED_COMMENT}",
                    f"    HostName {engine['instance_id']}",
                    f"    User {ssh_user}",
                    f"    ProxyCommand sh -c \"aws ssm start-session --target %h --document-name AWS-StartSSHSession --parameters 'portNumber=%p'\"",
                ]
            )

    # Write back
    config_path.write_text("\n".join(new_lines))
    config_path.chmod(0o600)

    if clean:
        console.print("[green]✓ Removed all managed SSH entries[/green]")
    else:
        console.print(
            f"[green]✓ Updated SSH config with {len(running_engines)} engines[/green]"
        )
        for engine in running_engines:
            user_display = (
                f"[dim]({engine['user']})[/dim]" if engine["user"] != username else ""
            )
            console.print(
                f"  • {engine['name']} → {engine['instance_id']} {user_display}"
            )


@engine_app.command("coffee")
def coffee(
    name_or_id: str = typer.Argument(help="Engine name or instance ID"),
    duration: str = typer.Argument("4h", help="Duration (e.g., 2h, 30m, 2h30m)"),
    cancel: bool = typer.Option(False, "--cancel", help="Cancel existing coffee lock instead of extending"),
):
    """Pour ☕ for an engine: keeps it awake for the given duration (or cancel)."""
    username = check_aws_sso()

    # Parse duration
    import re

    if not cancel:
        match = re.match(r"(?:(\d+)h)?(?:(\d+)m)?", duration)
        if not match or (not match.group(1) and not match.group(2)):
            console.print(f"[red]❌ Invalid duration format: {duration}[/red]")
            console.print("Use format like: 4h, 30m, 2h30m")
            raise typer.Exit(1)

        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds_total = (hours * 60 + minutes) * 60
        if seconds_total == 0:
            console.print("[red]❌ Duration must be greater than zero[/red]")
            raise typer.Exit(1)

    # Get all engines to resolve name
    response = make_api_request("GET", "/engines")
    if response.status_code != 200:
        console.print("[red]❌ Failed to fetch engines[/red]")
        raise typer.Exit(1)

    engines = response.json().get("engines", [])
    engine = resolve_engine(name_or_id, engines)

    if engine["state"].lower() != "running":
        console.print(f"[red]❌ Engine is not running (state: {engine['state']})[/red]")
        raise typer.Exit(1)

    if cancel:
        console.print(f"Cancelling coffee for [cyan]{engine['name']}[/cyan]…")
    else:
        console.print(f"Pouring coffee for [cyan]{engine['name']}[/cyan] for {duration}…")

    # Use SSM to run the engine keep-alive command
    ssm = boto3.client("ssm", region_name="us-east-1")
    try:
        response = ssm.send_command(
            InstanceIds=[engine["instance_id"]],
            DocumentName="AWS-RunShellScript",
            Parameters={
                "commands": [
                    ("/usr/local/bin/engine-coffee --cancel" if cancel else f"/usr/local/bin/engine-coffee {seconds_total}")
                ],
                "executionTimeout": ["60"],
            },
        )

        command_id = response["Command"]["CommandId"]

        # Wait for command to complete
        for _ in range(10):
            time.sleep(1)
            result = ssm.get_command_invocation(
                CommandId=command_id,
                InstanceId=engine["instance_id"],
            )
            if result["Status"] in ["Success", "Failed"]:
                break

        if result["Status"] == "Success":
            if cancel:
                console.print("[green]✓ Coffee cancelled – auto-shutdown re-enabled[/green]")
            else:
                console.print(f"[green]✓ Coffee poured for {duration}[/green]")
            console.print(
                "\n[dim]Note: Detached Docker containers (except dev containers) will also keep the engine awake.[/dim]"
            )
            console.print(
                "[dim]Use coffee for nohup operations or other background tasks.[/dim]"
            )
        else:
            console.print(
                f"[red]❌ Failed to manage coffee: {result.get('StatusDetails', 'Unknown error')}[/red]"
            )

    except ClientError as e:
        console.print(f"[red]❌ Failed to manage coffee: {e}[/red]")


@engine_app.command("resize")
def resize_engine(
    name_or_id: str = typer.Argument(help="Engine name or instance ID"),
    size: int = typer.Option(..., "--size", "-s", help="New size in GB"),
    online: bool = typer.Option(
        False, "--online", help="Resize while running (requires manual filesystem expansion)"
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force resize and detach all studios"
    ),
):
    """Resize an engine's boot disk."""
    check_aws_sso()

    # Get all engines to resolve name
    response = make_api_request("GET", "/engines")
    if response.status_code != 200:
        console.print("[red]❌ Failed to fetch engines[/red]")
        raise typer.Exit(1)

    engines = response.json().get("engines", [])
    engine = resolve_engine(name_or_id, engines)

    # Get current volume info to validate size
    ec2 = boto3.client("ec2", region_name="us-east-1")
    
    try:
        # Get instance details to find root volume
        instance_info = ec2.describe_instances(InstanceIds=[engine["instance_id"]])
        instance = instance_info["Reservations"][0]["Instances"][0]
        
        # Find root volume
        root_device = instance.get("RootDeviceName", "/dev/xvda")
        root_volume_id = None
        
        for bdm in instance.get("BlockDeviceMappings", []):
            if bdm["DeviceName"] == root_device:
                root_volume_id = bdm["Ebs"]["VolumeId"]
                break
        
        if not root_volume_id:
            console.print("[red]❌ Could not find root volume[/red]")
            raise typer.Exit(1)
        
        # Get current volume size
        volumes = ec2.describe_volumes(VolumeIds=[root_volume_id])
        current_size = volumes["Volumes"][0]["Size"]
        
        if size <= current_size:
            console.print(f"[red]❌ New size ({size}GB) must be larger than current size ({current_size}GB)[/red]")
            raise typer.Exit(1)
        
        console.print(f"[yellow]Resizing engine boot disk from {current_size}GB to {size}GB[/yellow]")
        
        # Check if we need to stop the instance
        if not online and engine["state"].lower() == "running":
            console.print("Stopping engine for offline resize...")
            stop_response = make_api_request(
                "POST", f"/engines/{engine['instance_id']}/stop", json_data={"detach_studios": False}
            )
            if stop_response.status_code != 200:
                console.print("[red]❌ Failed to stop engine[/red]")
                raise typer.Exit(1)
            
            # Wait for instance to stop
            console.print("Waiting for engine to stop...")
            waiter = ec2.get_waiter("instance_stopped")
            waiter.wait(InstanceIds=[engine["instance_id"]])
            console.print("[green]✓ Engine stopped[/green]")
        
        # Call the resize API
        console.print("Resizing volume...")
        resize_response = make_api_request(
            "POST", 
            f"/engines/{engine['instance_id']}/resize",
            json_data={"size": size, "detach_studios": force}
        )
        
        if resize_response.status_code == 409 and not force:
            # Engine has attached studios
            data = resize_response.json()
            attached_studios = data.get("attached_studios", [])

            console.print("\n[yellow]⚠️  This engine has attached studios:[/yellow]")
            for studio in attached_studios:
                console.print(f"  • {studio['user']} ({studio['studio_id']})")

            if Confirm.ask("\nDetach all studios and resize the engine?"):
                resize_response = make_api_request(
                    "POST",
                    f"/engines/{engine['instance_id']}/resize",
                    json_data={"size": size, "detach_studios": True}
                )
            else:
                console.print("Resize cancelled.")
                return
        
        if resize_response.status_code != 200:
            error = resize_response.json().get("error", "Unknown error")
            console.print(f"[red]❌ Failed to resize engine: {error}[/red]")
            raise typer.Exit(1)
        
        # Check if studios were detached
        data = resize_response.json()
        detached_studios = data.get("detached_studios", 0)
        if detached_studios > 0:
            console.print(f"[green]✓ Detached {detached_studios} studio(s) before resize[/green]")
        
        # Wait for modification to complete
        console.print("Waiting for volume modification to complete...")
        while True:
            mod_state = ec2.describe_volumes_modifications(VolumeIds=[root_volume_id])
            if not mod_state["VolumesModifications"]:
                break  # Modification complete
            
            modification = mod_state["VolumesModifications"][0]
            state = modification["ModificationState"]
            progress = modification.get("Progress", 0)
            
            # Show progress updates only for the resize phase
            if state == "modifying":
                console.print(f"[yellow]Progress: {progress}%[/yellow]")
            
            # Exit as soon as optimization starts (resize is complete)
            if state == "optimizing":
                console.print("[green]✓ Volume resized successfully[/green]")
                console.print("[dim]AWS is optimizing the volume in the background (no action needed).[/dim]")
                break
            
            if state == "completed":
                console.print("[green]✓ Volume resized successfully[/green]")
                break
            elif state == "failed":
                console.print("[red]❌ Volume modification failed[/red]")
                raise typer.Exit(1)
                
            time.sleep(2)  # Check more frequently for better UX
        
        # If offline resize, start the instance back up
        if not online and engine["state"].lower() == "running":
            console.print("Starting engine back up...")
            start_response = make_api_request("POST", f"/engines/{engine['instance_id']}/start")
            if start_response.status_code != 200:
                console.print("[yellow]⚠️  Failed to restart engine automatically[/yellow]")
                console.print(f"Please start it manually: [cyan]dh engine start {engine['name']}[/cyan]")
            else:
                console.print("[green]✓ Engine started[/green]")
                console.print("The filesystem will be automatically expanded on boot.")
        
        elif online and engine["state"].lower() == "running":
            console.print("\n[yellow]⚠️  Online resize complete. You must now expand the filesystem:[/yellow]")
            console.print(f"1. SSH into the engine: [cyan]ssh {engine['name']}[/cyan]")
            console.print("2. Find the root device: [cyan]lsblk[/cyan]")
            console.print("3. Expand the partition: [cyan]sudo growpart /dev/nvme0n1 1[/cyan] (adjust device name as needed)")
            console.print("4. Expand the filesystem: [cyan]sudo xfs_growfs /[/cyan]")
        
    except ClientError as e:
        console.print(f"[red]❌ Failed to resize engine: {e}[/red]")
        raise typer.Exit(1)


@engine_app.command("gami")
def create_ami(
    name_or_id: str = typer.Argument(
        help="Engine name or instance ID to create AMI from"
    ),
):
    """Create a Golden AMI from an engine."""
    check_aws_sso()

    # Get all engines to resolve name
    response = make_api_request("GET", "/engines")
    if response.status_code != 200:
        console.print("[red]❌ Failed to fetch engines[/red]")
        raise typer.Exit(1)

    engines = response.json().get("engines", [])
    engine = resolve_engine(name_or_id, engines)

    console.print(f"Creating AMI from engine [cyan]{engine['name']}[/cyan]...")

    # Get engine type from the engine
    engine_type = engine["engine_type"]

    # Generate AMI name
    date_str = datetime.now().strftime("%Y%m%d")
    ami_name = f"prewarmed-engine-{engine_type}-{date_str}"
    ami_description = (
        f"Amazon Linux 2023 with NVIDIA drivers, Docker, and pre-pulled dev container "
        f"image for {engine_type} engines"
    )

    console.print(f"AMI Name: [cyan]{ami_name}[/cyan]")
    console.print(f"Description: {ami_description}")
    console.print(
        "\n[yellow]⚠️  Important: This will reboot the engine to ensure a clean snapshot.[/yellow]"
    )

    if not Confirm.ask("\nContinue with AMI creation?"):
        console.print("AMI creation cancelled.")
        return

    # Create AMI using EC2 client
    ec2 = boto3.client("ec2", region_name="us-east-1")

    try:
        # First, we need to clean up the sentinel file via SSM
        console.print("Cleaning up bootstrap sentinel file...")
        ssm = boto3.client("ssm", region_name="us-east-1")

        cleanup_response = ssm.send_command(
            InstanceIds=[engine["instance_id"]],
            DocumentName="AWS-RunShellScript",
            Parameters={
                "commands": [
                    "sudo rm -f /opt/dayhoff/first_boot_complete.sentinel",
                    "history -c",
                    "sudo rm -rf /tmp/* /var/log/*",
                ],
                "executionTimeout": ["60"],
            },
        )

        # Wait for cleanup to complete
        command_id = cleanup_response["Command"]["CommandId"]
        for _ in range(10):
            time.sleep(1)
            result = ssm.get_command_invocation(
                CommandId=command_id,
                InstanceId=engine["instance_id"],
            )
            if result["Status"] in ["Success", "Failed"]:
                break

        if result["Status"] != "Success":
            console.print(
                "[yellow]⚠️  Warning: Cleanup command may have failed[/yellow]"
            )

        # Get instance details to find volumes to exclude
        instances = ec2.describe_instances(InstanceIds=[engine["instance_id"]])
        instance = instances["Reservations"][0]["Instances"][0]

        root_device = instance.get("RootDeviceName", "/dev/xvda")
        block_mappings = instance.get("BlockDeviceMappings", [])

        # Build exclusion list for non-root volumes
        block_device_mappings = []
        for mapping in block_mappings:
            device_name = mapping.get("DeviceName", "")
            if device_name != root_device:
                block_device_mappings.append(
                    {"DeviceName": device_name, "NoDevice": ""}
                )
                console.print(f"  Excluding volume at {device_name}")

        # Create the AMI
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                "Creating AMI (this will take several minutes)...", total=None
            )

            create_params = {
                "InstanceId": engine["instance_id"],
                "Name": ami_name,
                "Description": ami_description,
                "NoReboot": False,  # Important: reboot for clean snapshot
                "TagSpecifications": [
                    {
                        "ResourceType": "image",
                        "Tags": [
                            {"Key": "Environment", "Value": "dev"},
                            {"Key": "Type", "Value": "golden-ami"},
                            {"Key": "EngineType", "Value": engine_type},
                            {"Key": "Name", "Value": ami_name},
                        ],
                    }
                ],
            }

            if block_device_mappings:
                create_params["BlockDeviceMappings"] = block_device_mappings

            response = ec2.create_image(**create_params)

            ami_id = response["ImageId"]
            console.print(f"[green]✓ AMI creation initiated![/green]")
            console.print(f"AMI ID: [cyan]{ami_id}[/cyan]")

            # Restore the source engine to a normal state
            console.print("Restoring source engine state...")
            restore_response = ssm.send_command(
                InstanceIds=[engine["instance_id"]],
                DocumentName="AWS-RunShellScript",
                Parameters={
                    "commands": [
                        "sudo touch /opt/dayhoff/first_boot_complete.sentinel",
                        "sudo systemctl restart engine-idle-detector.timer",
                    ],
                    "executionTimeout": ["60"],
                },
            )

            # Quick wait to see if it failed immediately
            time.sleep(1)
            restore_command_id = restore_response["Command"]["CommandId"]
            result = ssm.get_command_invocation(
                CommandId=restore_command_id,
                InstanceId=engine["instance_id"],
            )
            if result["Status"] not in ["Pending", "InProgress", "Success"]:
                console.print(
                    "[yellow]⚠️  Warning: Failed to restore source engine state.[/yellow]"
                )
            else:
                console.print(
                    "[green]✓ Source engine restored to normal operation.[/green]"
                )

            console.print(
                "\n[dim]The AMI creation process will continue in the background.[/dim]"
            )
            console.print(
                "[dim]You can monitor progress in the EC2 Console under 'AMIs'.[/dim]"
            )
            console.print(
                f"\nOnce complete, run [cyan]terraform apply[/cyan] in "
                f"terraform/environments/dev to use the new AMI."
            )

    except ClientError as e:
        console.print(f"[red]❌ Failed to create AMI: {e}[/red]")
        raise typer.Exit(1)


# ==================== STUDIO COMMANDS ====================


def get_user_studio(username: str) -> Optional[Dict]:
    """Get the current user's studio."""
    response = make_api_request("GET", "/studios")
    if response.status_code != 200:
        return None

    studios = response.json().get("studios", [])
    user_studios = [s for s in studios if s["user"] == username]

    return user_studios[0] if user_studios else None


@studio_app.command("create")
def create_studio(
    size_gb: int = typer.Option(50, "--size", "-s", help="Studio size in GB"),
):
    """Create a new studio for the current user."""
    username = check_aws_sso()

    # Check if user already has a studio
    existing = get_user_studio(username)
    if existing:
        console.print(
            f"[yellow]You already have a studio: {existing['studio_id']}[/yellow]"
        )
        return

    console.print(f"Creating {size_gb}GB studio for user [cyan]{username}[/cyan]...")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("Creating studio volume...", total=None)

        response = make_api_request(
            "POST",
            "/studios",
            json_data={"user": username, "size_gb": size_gb},
        )

    if response.status_code == 201:
        data = response.json()
        console.print(f"[green]✓ Studio created successfully![/green]")
        console.print(f"Studio ID: [cyan]{data['studio_id']}[/cyan]")
        console.print(f"Size: {data['size_gb']}GB")
        console.print(f"\nNext step: [cyan]dh studio attach <engine-name>[/cyan]")
    else:
        error = response.json().get("error", "Unknown error")
        console.print(f"[red]❌ Failed to create studio: {error}[/red]")


@studio_app.command("status")
def studio_status(
    user: Optional[str] = typer.Option(None, "--user", "-u", help="Check status for a different user (admin only)"),
):
    """Show status of your studio."""
    username = check_aws_sso()
    
    # Use specified user if provided, otherwise use current user
    target_user = user if user else username
    
    # Add warning when checking another user's studio
    if target_user != username:
        console.print(f"[yellow]⚠️  Checking studio status for user: {target_user}[/yellow]")
    
    studio = get_user_studio(target_user)
    if not studio:
        if target_user == username:
            console.print("[yellow]You don't have a studio yet.[/yellow]")
            console.print("Create one with: [cyan]dh studio create[/cyan]")
        else:
            console.print(f"[yellow]User {target_user} doesn't have a studio.[/yellow]")
        return

    # Create status panel
    # Format status with colors
    status = studio["status"]
    if status == "in-use":
        status_display = "[bright_blue]attached[/bright_blue]"
    elif status in ["attaching", "detaching"]:
        status_display = f"[yellow]{status}[/yellow]"
    else:
        status_display = f"[green]{status}[/green]"

    status_lines = [
        f"[bold]Studio ID:[/bold]    {studio['studio_id']}",
        f"[bold]User:[/bold]         {studio['user']}",
        f"[bold]Status:[/bold]       {status_display}",
        f"[bold]Size:[/bold]         {studio['size_gb']}GB",
        f"[bold]Created:[/bold]      {studio['creation_date']}",
    ]

    if studio.get("attached_vm_id"):
        status_lines.append(f"[bold]Attached to:[/bold]  {studio['attached_vm_id']}")

        # Try to get engine details
        response = make_api_request("GET", "/engines")
        if response.status_code == 200:
            engines = response.json().get("engines", [])
            attached_engine = next(
                (e for e in engines if e["instance_id"] == studio["attached_vm_id"]),
                None,
            )
            if attached_engine:
                status_lines.append(
                    f"[bold]Engine Name:[/bold]  {attached_engine['name']}"
                )

    panel = Panel(
        "\n".join(status_lines),
        title="Studio Details",
        border_style="blue",
    )
    console.print(panel)


@studio_app.command("attach")
def attach_studio(
    engine_name_or_id: str = typer.Argument(help="Engine name or instance ID"),
    user: Optional[str] = typer.Option(None, "--user", "-u", help="Attach a different user's studio (admin only)"),
):
    """Attach your studio to an engine."""
    username = check_aws_sso()
    
    # Use specified user if provided, otherwise use current user
    target_user = user if user else username
    
    # Add confirmation when attaching another user's studio
    if target_user != username:
        console.print(f"[yellow]⚠️  Managing studio for user: {target_user}[/yellow]")
        if not Confirm.ask(f"Are you sure you want to attach {target_user}'s studio?"):
            console.print("Operation cancelled.")
            return

    # Get user's studio
    studio = get_user_studio(target_user)
    if not studio:
        if target_user == username:
            console.print("[yellow]You don't have a studio yet.[/yellow]")
            if Confirm.ask("Would you like to create one now?"):
                size = IntPrompt.ask("Studio size (GB)", default=50)
                response = make_api_request(
                    "POST",
                    "/studios",
                    json_data={"user": username, "size_gb": size},
                )
                if response.status_code != 201:
                    console.print("[red]❌ Failed to create studio[/red]")
                    raise typer.Exit(1)
                studio = response.json()
                studio["studio_id"] = studio["studio_id"]  # Normalize key
            else:
                raise typer.Exit(0)
        else:
            console.print(f"[red]❌ User {target_user} doesn't have a studio.[/red]")
            raise typer.Exit(1)

    # Check if already attached
    if studio.get("status") == "in-use":
        console.print(
            f"[yellow]Studio is already attached to {studio.get('attached_vm_id')}[/yellow]"
        )
        if not Confirm.ask("Detach and reattach to new engine?"):
            return
        # Detach first
        response = make_api_request("POST", f"/studios/{studio['studio_id']}/detach")
        if response.status_code != 200:
            console.print("[red]❌ Failed to detach studio[/red]")
            raise typer.Exit(1)

    # Get all engines to resolve name
    response = make_api_request("GET", "/engines")
    if response.status_code != 200:
        console.print("[red]❌ Failed to fetch engines[/red]")
        raise typer.Exit(1)

    engines = response.json().get("engines", [])
    engine = resolve_engine(engine_name_or_id, engines)

    if engine["state"].lower() != "running":
        console.print(f"[yellow]⚠️  Engine is {engine['state']}[/yellow]")
        if engine["state"].lower() == "stopped" and Confirm.ask(
            "Start the engine first?"
        ):
            response = make_api_request(
                "POST", f"/engines/{engine['instance_id']}/start"
            )
            if response.status_code != 200:
                console.print("[red]❌ Failed to start engine[/red]")
                raise typer.Exit(1)
            console.print("[green]✓ Engine started[/green]")
            console.print("Waiting for engine to be ready...")
            import time

            time.sleep(10)
        else:
            raise typer.Exit(1)

    # Get SSH key
    try:
        public_key = get_ssh_public_key()
    except FileNotFoundError as e:
        console.print(f"[red]❌ {e}[/red]")
        raise typer.Exit(1)

    console.print(f"Attaching studio to engine [cyan]{engine['name']}[/cyan]...")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Attaching studio...", total=100)

        response = make_api_request(
            "POST",
            f"/studios/{studio['studio_id']}/attach",
            json_data={
                "vm_id": engine["instance_id"],
                "user": target_user,  # Use target_user instead of username
                "public_key": public_key,
            },
        )

        progress.update(task, completed=100)

    if response.status_code == 200:
        console.print(f"[green]✓ Studio attached successfully![/green]")

        # Update SSH config - use target_user for the connection
        update_ssh_config_entry(engine["name"], engine["instance_id"], target_user)
        console.print(f"[green]✓ SSH config updated[/green]")
        console.print(f"\nConnect with: [cyan]ssh {engine['name']}[/cyan]")
        console.print(f"Files are at: [cyan]/studios/{target_user}[/cyan]")
    else:
        error = response.json().get("error", "Unknown error")
        console.print(f"[red]❌ Failed to attach studio: {error}[/red]")


@studio_app.command("detach")
def detach_studio(
    user: Optional[str] = typer.Option(None, "--user", "-u", help="Detach a different user's studio (admin only)"),
):
    """Detach your studio from its current engine."""
    username = check_aws_sso()
    
    # Use specified user if provided, otherwise use current user
    target_user = user if user else username
    
    # Add confirmation when detaching another user's studio
    if target_user != username:
        console.print(f"[yellow]⚠️  Managing studio for user: {target_user}[/yellow]")
        if not Confirm.ask(f"Are you sure you want to detach {target_user}'s studio?"):
            console.print("Operation cancelled.")
            return

    studio = get_user_studio(target_user)
    if not studio:
        if target_user == username:
            console.print("[yellow]You don't have a studio.[/yellow]")
        else:
            console.print(f"[yellow]User {target_user} doesn't have a studio.[/yellow]")
        return

    if studio.get("status") != "in-use":
        if target_user == username:
            console.print("[yellow]Your studio is not attached to any engine.[/yellow]")
        else:
            console.print(f"[yellow]{target_user}'s studio is not attached to any engine.[/yellow]")
        return

    console.print(f"Detaching studio from {studio.get('attached_vm_id')}...")

    response = make_api_request("POST", f"/studios/{studio['studio_id']}/detach")

    if response.status_code == 200:
        console.print(f"[green]✓ Studio detached successfully![/green]")
    else:
        error = response.json().get("error", "Unknown error")
        console.print(f"[red]❌ Failed to detach studio: {error}[/red]")


@studio_app.command("delete")
def delete_studio(
    user: Optional[str] = typer.Option(None, "--user", "-u", help="Delete a different user's studio (admin only)"),
):
    """Delete your studio permanently."""
    username = check_aws_sso()
    
    # Use specified user if provided, otherwise use current user
    target_user = user if user else username
    
    # Extra warning when deleting another user's studio
    if target_user != username:
        console.print(f"[red]⚠️  ADMIN ACTION: Deleting studio for user: {target_user}[/red]")

    studio = get_user_studio(target_user)
    if not studio:
        if target_user == username:
            console.print("[yellow]You don't have a studio to delete.[/yellow]")
        else:
            console.print(f"[yellow]User {target_user} doesn't have a studio to delete.[/yellow]")
        return

    console.print(
        "[red]⚠️  WARNING: This will permanently delete the studio and all data![/red]"
    )
    console.print(f"Studio ID: {studio['studio_id']}")
    console.print(f"User: {target_user}")
    console.print(f"Size: {studio['size_gb']}GB")

    # Multiple confirmations
    if not Confirm.ask(f"\nAre you sure you want to delete {target_user}'s studio?" if target_user != username else "\nAre you sure you want to delete your studio?"):
        console.print("Deletion cancelled.")
        return

    if not Confirm.ask("[red]This action cannot be undone. Continue?[/red]"):
        console.print("Deletion cancelled.")
        return

    typed_confirm = Prompt.ask('Type "DELETE" to confirm permanent deletion')
    if typed_confirm != "DELETE":
        console.print("Deletion cancelled.")
        return

    response = make_api_request("DELETE", f"/studios/{studio['studio_id']}")

    if response.status_code == 200:
        console.print(f"[green]✓ Studio deleted successfully![/green]")
    else:
        error = response.json().get("error", "Unknown error")
        console.print(f"[red]❌ Failed to delete studio: {error}[/red]")


@studio_app.command("list")
def list_studios(
    all_users: bool = typer.Option(
        False, "--all", "-a", help="Show all users' studios"
    ),
):
    """List studios."""
    username = check_aws_sso()

    response = make_api_request("GET", "/studios")

    if response.status_code == 200:
        studios = response.json().get("studios", [])

        if not studios:
            console.print("No studios found.")
            return

        # Get all engines to map instance IDs to names
        engines_response = make_api_request("GET", "/engines")
        engines = {}
        if engines_response.status_code == 200:
            for engine in engines_response.json().get("engines", []):
                engines[engine["instance_id"]] = engine["name"]

        # Create table
        table = Table(title="Studios", box=box.ROUNDED)
        table.add_column("Studio ID", style="cyan")
        table.add_column("User")
        table.add_column("Status")
        table.add_column("Size", justify="right")
        table.add_column("Disk Usage", justify="right")
        table.add_column("Attached To")

        for studio in studios:
            # Change status display
            if studio["status"] == "in-use":
                status_display = "[bright_blue]attached[/bright_blue]"
            elif studio["status"] in ["attaching", "detaching"]:
                status_display = "[yellow]" + studio["status"] + "[/yellow]"
            else:
                status_display = "[green]available[/green]"

            # Format attached engine info
            attached_to = "-"
            disk_usage = "?/?"
            if studio.get("attached_vm_id"):
                vm_id = studio["attached_vm_id"]
                engine_name = engines.get(vm_id, "unknown")
                attached_to = f"{engine_name} ({vm_id})"
                
                # Try to get disk usage if attached
                if studio["status"] == "in-use":
                    usage = get_studio_disk_usage_via_ssm(vm_id, studio["user"])
                    if usage:
                        disk_usage = usage

            table.add_row(
                studio["studio_id"],
                studio["user"],
                status_display,
                f"{studio['size_gb']}GB",
                disk_usage,
                attached_to,
            )

        console.print(table)
    else:
        error = response.json().get("error", "Unknown error")
        console.print(f"[red]❌ Failed to list studios: {error}[/red]")


@studio_app.command("reset")
def reset_studio(
    user: Optional[str] = typer.Option(None, "--user", "-u", help="Reset a different user's studio"),
):
    """Reset a stuck studio (admin operation)."""
    username = check_aws_sso()
    
    # Use specified user if provided, otherwise use current user
    target_user = user if user else username
    
    # Add warning when resetting another user's studio
    if target_user != username:
        console.print(f"[yellow]⚠️  Resetting studio for user: {target_user}[/yellow]")

    studio = get_user_studio(target_user)
    if not studio:
        if target_user == username:
            console.print("[yellow]You don't have a studio.[/yellow]")
        else:
            console.print(f"[yellow]User {target_user} doesn't have a studio.[/yellow]")
        return

    console.print(f"[yellow]⚠️  This will force-reset the studio state[/yellow]")
    console.print(f"Current status: {studio['status']}")
    if studio.get("attached_vm_id"):
        console.print(f"Listed as attached to: {studio['attached_vm_id']}")

    if not Confirm.ask("\nReset studio state?"):
        console.print("Reset cancelled.")
        return

    # Direct DynamoDB update
    console.print("Resetting studio state...")

    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.Table("dev-studios")

    try:
        # Check if volume is actually attached
        ec2 = boto3.client("ec2", region_name="us-east-1")
        volumes = ec2.describe_volumes(VolumeIds=[studio["studio_id"]])

        if volumes["Volumes"]:
            volume = volumes["Volumes"][0]
            attachments = volume.get("Attachments", [])
            if attachments:
                console.print(
                    f"[red]Volume is still attached to {attachments[0]['InstanceId']}![/red]"
                )
                if Confirm.ask("Force-detach the volume?"):
                    ec2.detach_volume(
                        VolumeId=studio["studio_id"],
                        InstanceId=attachments[0]["InstanceId"],
                        Force=True,
                    )
                    console.print("Waiting for volume to detach...")
                    waiter = ec2.get_waiter("volume_available")
                    waiter.wait(VolumeIds=[studio["studio_id"]])

        # Reset in DynamoDB
        table.update_item(
            Key={"studio_id": studio["studio_id"]},
            UpdateExpression="SET #status = :status, attached_vm_id = :vm_id, attached_device = :device",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={
                ":status": "available",
                ":vm_id": None,
                ":device": None,
            },
        )

        console.print(f"[green]✓ Studio reset to available state![/green]")

    except ClientError as e:
        console.print(f"[red]❌ Failed to reset studio: {e}[/red]")


@studio_app.command("resize")
def resize_studio(
    size: int = typer.Option(..., "--size", "-s", help="New size in GB"),
    user: Optional[str] = typer.Option(None, "--user", "-u", help="Resize a different user's studio (admin only)"),
):
    """Resize your studio volume (requires detachment)."""
    username = check_aws_sso()
    
    # Use specified user if provided, otherwise use current user
    target_user = user if user else username
    
    # Add warning when resizing another user's studio
    if target_user != username:
        console.print(f"[yellow]⚠️  Resizing studio for user: {target_user}[/yellow]")

    studio = get_user_studio(target_user)
    if not studio:
        if target_user == username:
            console.print("[yellow]You don't have a studio yet.[/yellow]")
        else:
            console.print(f"[yellow]User {target_user} doesn't have a studio.[/yellow]")
        return

    current_size = studio["size_gb"]
    
    if size <= current_size:
        console.print(f"[red]❌ New size ({size}GB) must be larger than current size ({current_size}GB)[/red]")
        raise typer.Exit(1)

    # Check if studio is attached
    if studio["status"] == "in-use":
        console.print("[yellow]⚠️  Studio must be detached before resizing[/yellow]")
        console.print(f"Currently attached to: {studio.get('attached_vm_id')}")
        
        if not Confirm.ask("\nDetach studio and proceed with resize?"):
            console.print("Resize cancelled.")
            return
        
        # Detach the studio
        console.print("Detaching studio...")
        response = make_api_request("POST", f"/studios/{studio['studio_id']}/detach")
        if response.status_code != 200:
            console.print("[red]❌ Failed to detach studio[/red]")
            raise typer.Exit(1)
        
        console.print("[green]✓ Studio detached[/green]")
        
        # Wait a moment for detachment to complete
        time.sleep(5)

    console.print(f"[yellow]Resizing studio from {current_size}GB to {size}GB[/yellow]")

    # Call the resize API
    resize_response = make_api_request(
        "POST",
        f"/studios/{studio['studio_id']}/resize",
        json_data={"size": size}
    )
    
    if resize_response.status_code != 200:
        error = resize_response.json().get("error", "Unknown error")
        console.print(f"[red]❌ Failed to resize studio: {error}[/red]")
        raise typer.Exit(1)
    
    # Wait for volume modification to complete
    ec2 = boto3.client("ec2", region_name="us-east-1")
    console.print("Resizing volume...")
    
    # Track progress
    last_progress = 0
    
    while True:
        try:
            mod_state = ec2.describe_volumes_modifications(VolumeIds=[studio["studio_id"]])
            if not mod_state["VolumesModifications"]:
                break  # Modification complete
            
            modification = mod_state["VolumesModifications"][0]
            state = modification["ModificationState"]
            progress = modification.get("Progress", 0)
            
            # Show progress updates only for the resize phase
            if state == "modifying" and progress > last_progress:
                console.print(f"[yellow]Progress: {progress}%[/yellow]")
                last_progress = progress
            
            # Exit as soon as optimization starts (resize is complete)
            if state == "optimizing":
                console.print(f"[green]✓ Studio resized successfully to {size}GB![/green]")
                console.print("[dim]AWS is optimizing the volume in the background (no action needed).[/dim]")
                break
            
            if state == "completed":
                console.print(f"[green]✓ Studio resized successfully to {size}GB![/green]")
                break
            elif state == "failed":
                console.print("[red]❌ Volume modification failed[/red]")
                raise typer.Exit(1)
            
            time.sleep(2)  # Check more frequently for better UX
            
        except ClientError:
            # Modification might be complete
            console.print(f"[green]✓ Studio resized successfully to {size}GB![/green]")
            break
    
    console.print("\n[dim]The filesystem will be automatically expanded when you next attach the studio.[/dim]")
    console.print(f"To attach: [cyan]dh studio attach <engine-name>[/cyan]")

# ================= Idle timeout command =================


@engine_app.command("idle")
def idle_timeout_cmd(
    name_or_id: str = typer.Argument(help="Engine name or instance ID"),
    set: Optional[str] = typer.Option(None, "--set", "-s", help="New timeout (e.g., 2h30m, 45m)")
):
    """Show or set the engine idle-detector timeout."""
    check_aws_sso()

    # Resolve engine
    response = make_api_request("GET", "/engines")
    if response.status_code != 200:
        console.print("[red]❌ Failed to fetch engines[/red]")
        raise typer.Exit(1)

    engines = response.json().get("engines", [])
    engine = resolve_engine(name_or_id, engines)

    ssm = boto3.client("ssm", region_name="us-east-1")

    if set is None:
        # Show current
        resp = ssm.send_command(
            InstanceIds=[engine["instance_id"]],
            DocumentName="AWS-RunShellScript",
            Parameters={"commands": ["grep -E '^IDLE_TIMEOUT_SECONDS=' /etc/engine.env || echo 'IDLE_TIMEOUT_SECONDS=1800'"], "executionTimeout": ["10"]},
        )
        cid = resp["Command"]["CommandId"]
        time.sleep(1)
        inv = ssm.get_command_invocation(CommandId=cid, InstanceId=engine["instance_id"])
        if inv["Status"] == "Success":
            line = inv["StandardOutputContent"].strip()
            secs = int(line.split("=")[1]) if "=" in line else 1800
            console.print(f"Current idle timeout: {secs//60}m ({secs} seconds)")
        else:
            console.print("[red]❌ Could not retrieve idle timeout[/red]")
        return

    # ----- set new value -----
    m = re.match(r"^(?:(\d+)h)?(?:(\d+)m)?$", set)
    if not m:
        console.print("[red]❌ Invalid duration format. Use e.g. 2h, 45m, 1h30m[/red]")
        raise typer.Exit(1)
    hours = int(m.group(1) or 0)
    minutes = int(m.group(2) or 0)
    seconds = hours * 3600 + minutes * 60
    if seconds == 0:
        console.print("[red]❌ Duration must be greater than zero[/red]")
        raise typer.Exit(1)

    console.print(f"Setting idle timeout to {set} ({seconds} seconds)…")

    cmd = (
        "sudo sed -i '/^IDLE_TIMEOUT_SECONDS=/d' /etc/engine.env && "
        f"echo 'IDLE_TIMEOUT_SECONDS={seconds}' | sudo tee -a /etc/engine.env >/dev/null && "
        "sudo systemctl restart engine-idle-detector.timer"
    )

    resp = ssm.send_command(
        InstanceIds=[engine["instance_id"]],
        DocumentName="AWS-RunShellScript",
        Parameters={"commands": [cmd], "executionTimeout": ["60"]},
    )
    cid = resp["Command"]["CommandId"]
    time.sleep(2)
    console.print(f"[green]✓ Idle timeout updated to {set}[/green]")

# Add this near the end, after the idle-timeout command

@engine_app.command("debug")
def debug_engine(
    name_or_id: str = typer.Argument(help="Engine name or instance ID"),
):
    """Debug engine bootstrap status and files."""
    check_aws_sso()

    # Resolve engine
    response = make_api_request("GET", "/engines")
    if response.status_code != 200:
        console.print("[red]❌ Failed to fetch engines[/red]")
        raise typer.Exit(1)

    engines = response.json().get("engines", [])
    engine = resolve_engine(name_or_id, engines)

    console.print(f"[bold]Debug info for {engine['name']}:[/bold]\n")

    ssm = boto3.client("ssm", region_name="us-east-1")
    
    # Check multiple files and systemd status
    checks = [
        ("Stage file", "cat /opt/dayhoff/state/engine-init.stage 2>/dev/null || cat /var/run/engine-init.stage 2>/dev/null || echo 'MISSING'"),
        ("Health file", "cat /opt/dayhoff/state/engine-health.json 2>/dev/null || cat /var/run/engine-health.json 2>/dev/null || echo 'MISSING'"),
        ("Sentinel file", "ls -la /opt/dayhoff/first_boot_complete.sentinel 2>/dev/null || echo 'MISSING'"),
        ("Setup service", "systemctl status setup-aws-vm.service --no-pager || echo 'Service not found'"),
        ("Bootstrap log tail", "tail -20 /var/log/engine-setup.log 2>/dev/null || echo 'No log'"),
        ("Environment file", "cat /etc/engine.env 2>/dev/null || echo 'MISSING'"),
    ]
    
    for name, cmd in checks:
        try:
            resp = ssm.send_command(
                InstanceIds=[engine["instance_id"]],
                DocumentName="AWS-RunShellScript",
                Parameters={"commands": [cmd], "executionTimeout": ["10"]},
            )
            cid = resp["Command"]["CommandId"]
            time.sleep(1)
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=engine["instance_id"])
            
            if inv["Status"] == "Success":
                output = inv["StandardOutputContent"].strip()
                console.print(f"[cyan]{name}:[/cyan]")
                console.print(f"[dim]{output}[/dim]\n")
            else:
                console.print(f"[cyan]{name}:[/cyan] [red]FAILED[/red]\n")
                
        except Exception as e:
            console.print(f"[cyan]{name}:[/cyan] [red]ERROR: {e}[/red]\n")
