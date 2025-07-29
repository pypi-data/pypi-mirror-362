#!/usr/bin/env python3
"""
ACOLYTE CLI - Command Line Interface
Global tool for managing ACOLYTE in user projects
"""

import asyncio
import hashlib
import os
import sys
import shutil
import subprocess
import time
from pathlib import Path
from typing import Optional, Dict, Any

import click
import yaml
import requests
from acolyte.install.common.port_manager import PortManager
from acolyte.install.common.docker import check_docker_ready
from acolyte.console import logs

# LAZY IMPORTS - Only import when needed to speed up simple commands
logger = None


def get_logger():
    """Get logger instance lazily - only import when actually needed"""
    global logger
    if logger is None:
        from acolyte.core.logging import logger as _logger

        logger = _logger
    return logger


class ProjectManager:
    """Manages ACOLYTE projects and their configurations"""

    def __init__(self):
        self.global_dir = self._get_global_dir()
        self.projects_dir = self.global_dir / "projects"

        # Initialize global directory structure if needed
        self._ensure_global_structure()

    def _ensure_global_structure(self):
        """Ensure ACOLYTE global directory structure exists"""
        # Create directories
        self.global_dir.mkdir(parents=True, exist_ok=True)
        self.projects_dir.mkdir(exist_ok=True)

        # Create other necessary directories
        # (self.global_dir / "models").mkdir(exist_ok=True)  # REMOVED: Not used
        (self.global_dir / "logs").mkdir(exist_ok=True)

        # Copy essential files if this is first run
        if not (self.global_dir / ".initialized").exists():
            self._first_run_setup()

    def _first_run_setup(self):
        """Setup ACOLYTE on first run after pip install"""
        # Only log if we're actually doing initialization work
        log = get_logger()
        log.info("First run detected, initializing ACOLYTE...")

        # REMOVED: Copy example configurations - Not used
        # examples_dir = Path(__file__).parent.parent.parent / "examples"
        # if examples_dir.exists():
        #     dest_examples = self.global_dir / "examples"
        #     if dest_examples.exists():
        #         shutil.rmtree(dest_examples)
        #     shutil.copytree(examples_dir, dest_examples)

        # Mark as initialized
        (self.global_dir / ".initialized").touch()
        log.info(f"ACOLYTE initialized at {self.global_dir}")

    def _get_global_dir(self) -> Path:
        """Get the global ACOLYTE directory"""
        if os.name == 'nt':  # Windows
            return Path.home() / ".acolyte"
        else:  # Linux/Mac
            # Check if running from development or installed
            if 'ACOLYTE_DEV' in os.environ:
                return Path.home() / ".acolyte-dev"
            return Path.home() / ".acolyte"

    def get_project_id(self, project_path: Path) -> str:
        """Generate unique project ID from path and git remote"""
        # Try to get git remote
        git_remote = ""
        git_dir = project_path / ".git"
        if git_dir.exists():
            try:
                result = subprocess.run(
                    ["git", "remote", "get-url", "origin"],
                    cwd=project_path,
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    git_remote = result.stdout.strip()
            except Exception:
                pass

        # Generate hash from absolute path + git remote
        abs_path = str(project_path.resolve())
        unique_string = f"{git_remote}:{abs_path}"
        project_id = hashlib.sha256(unique_string.encode()).hexdigest()[:12]

        return project_id

    def get_project_dir(self, project_id: str) -> Path:
        """Get the directory for a specific project"""
        return self.projects_dir / project_id

    def is_project_initialized(self, project_path: Path) -> bool:
        """Check if project is already initialized"""
        project_file = project_path / ".acolyte.project"
        return project_file.exists()

    def load_project_info(self, project_path: Path) -> Optional[Dict[str, Any]]:
        """Load project info from .acolyte.project"""
        project_file = project_path / ".acolyte.project"
        if not project_file.exists():
            return None

        try:
            with open(project_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            # Only log errors when we have actual errors
            log = get_logger()
            log.error(f"Failed to load project info: {e}")
            return None

    def save_project_info(self, project_path: Path, info: Dict[str, Any]) -> bool:
        """Save project info to .acolyte.project"""
        project_file = project_path / ".acolyte.project"
        try:
            with open(project_file, 'w') as f:
                yaml.dump(info, f, default_flow_style=False, sort_keys=False)
            return True
        except Exception as e:
            # Only log errors when we have actual errors
            log = get_logger()
            log.error(f"Failed to save project info: {e}")
            return False


def validate_project_directory(ctx, param, value):
    """Validate that we're in a valid project directory"""
    project_path = Path(value or ".")

    # Check if it's a git repository or has project files
    markers = [
        ".git",
        "package.json",
        "pyproject.toml",
        "setup.py",  # Python
        "Cargo.toml",  # Rust
        "go.mod",  # Go
        "pom.xml",
        "build.gradle",  # Java
        "composer.json",  # PHP
        "Gemfile",  # Ruby
    ]

    has_marker = any((project_path / marker).exists() for marker in markers)

    if not has_marker:
        raise click.BadParameter(
            "Not a valid project directory. Please run from a project with version control or project file."
        )

    return project_path


def detect_docker_compose_cmd() -> list[str]:
    """Detect the correct docker compose command"""
    # Try docker compose (newer versions)
    try:
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return ["docker", "compose"]
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Fallback to docker-compose (older versions)
    try:
        result = subprocess.run(
            ["docker-compose", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return ["docker-compose"]
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    raise click.ClickException(
        "Docker Compose not found. Please install Docker Desktop or docker-compose."
    )


def ensure_acolyte_model_exists(config: Dict[str, Any], infra_dir: Path, console) -> bool:
    """
    Ensure the acolyte model exists in Ollama.
    This function handles model creation in a centralized way.

    Returns:
        True if model exists or was created successfully, False otherwise
    """
    try:
        # Check if acolyte:latest exists in the container
        model_check = subprocess.run(
            ["docker", "exec", "acolyte-ollama", "ollama", "list"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
        )

        if model_check.returncode != 0:
            console.print("[yellow]⚠ Could not check Ollama models in container")
            return False

        if "acolyte:latest" in model_check.stdout:
            console.print(
                "[green]✓ Model acolyte:latest already exists in container (from install or previous run)"
            )
            return True

        # If not, check if the model exists in the host Ollama (from install)
        host_model_exists = False
        try:
            host_model_check = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
            )
            if host_model_check.returncode == 0 and "acolyte" in host_model_check.stdout:
                host_model_exists = True
        except FileNotFoundError:
            # Ollama CLI not installed on host; ignore and proceed to build inside container
            pass
        if host_model_exists:
            console.print(
                "[green]✓ Model acolyte found in host Ollama. Attempting to export and import into container..."
            )
            # Export model from host
            export_result = subprocess.run(["ollama", "export", "acolyte"], capture_output=True)
            if export_result.returncode == 0:
                try:
                    # Copy exported model to container (assume default path)
                    with open("acolyte.ollama", "wb") as f:
                        f.write(export_result.stdout)
                    copy_result = subprocess.run(
                        ["docker", "cp", "acolyte.ollama", "acolyte-ollama:/tmp/acolyte.ollama"],
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        errors='replace',
                    )
                    if copy_result.returncode == 0:
                        # Import model in container
                        import_result = subprocess.run(
                            [
                                "docker",
                                "exec",
                                "acolyte-ollama",
                                "ollama",
                                "import",
                                "/tmp/acolyte.ollama",
                            ],
                            text=True,
                            encoding='utf-8',
                            errors='replace',
                        )
                        if import_result.returncode == 0:
                            console.print(
                                "[green]✓ Model acolyte imported into container successfully"
                            )
                            return True
                        else:
                            console.print(
                                "[yellow]⚠ Failed to import model into container, will try to build from Modelfile"
                            )
                    else:
                        console.print(
                            "[yellow]⚠ Could not copy exported model to container, will try to build from Modelfile"
                        )
                finally:
                    try:
                        os.remove("acolyte.ollama")
                    except Exception:
                        pass
            else:
                console.print(
                    "[yellow]⚠ Failed to export model from host, will try to build from Modelfile"
                )
        else:
            console.print(
                "[yellow]⚠ Model acolyte not found in host Ollama, will try to build from Modelfile"
            )

        # Model doesn't exist, create it from Modelfile in container
        console.print("[yellow]⚠ Model 'acolyte:latest' not found, creating in container...")
        model_name = config.get('model', {}).get('name', 'qwen2.5-coder:3b')
        if model_name.startswith('acolyte:'):
            model_name = 'qwen2.5-coder:3b'  # Default base model
        # Pull base model if needed
        if model_name not in model_check.stdout:
            console.print(f"[dim]• Pulling base model {model_name} in container...[/dim]")
            pull_result = subprocess.run(
                ["docker", "exec", "acolyte-ollama", "ollama", "pull", model_name],
                text=True,
                encoding='utf-8',
                errors='replace',
            )
            if pull_result.returncode != 0:
                console.print(f"[bold red]✗ Failed to pull {model_name} in container[/bold red]")
                return False
            console.print(f"[green]✓ Base model {model_name} ready in container")
        # Copy Modelfile to container
        modelfile_path = infra_dir / "Modelfile"
        if not modelfile_path.exists():
            console.print("[yellow]⚠ Modelfile not found at expected location")
            console.print(f"[dim]Expected: {modelfile_path}[/dim]")
            return False
        copy_result = subprocess.run(
            ["docker", "cp", str(modelfile_path), "acolyte-ollama:/tmp/Modelfile"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
        )
        if copy_result.returncode != 0:
            console.print("[yellow]⚠ Could not copy Modelfile to container")
            return False
        # Create the model in container
        console.print("[dim]• Creating acolyte:latest model in container...[/dim]")
        create_result = subprocess.run(
            [
                "docker",
                "exec",
                "acolyte-ollama",
                "ollama",
                "create",
                "acolyte:latest",
                "-f",
                "/tmp/Modelfile",
            ],
            text=True,
            encoding='utf-8',
            errors='replace',
        )
        if create_result.returncode == 0:
            console.print("[green]✓ Model acolyte:latest created successfully in container")
            return True
        else:
            console.print(
                "[bold red]✗ Failed to create acolyte:latest model in container[/bold red]"
            )
            return False
    except Exception as e:
        console.print(f"[bold red]✗ Error creating or importing model: {e}[/bold red]")
        return False


# Lazy version loading for CLI
def _get_version():
    try:
        from acolyte._version import __version__

        return __version__
    except Exception:
        return "0.1.5"  # fallback


@click.group()
@click.version_option(version=_get_version(), prog_name="ACOLYTE")
def cli():
    """
    ACOLYTE - AI Programming Assistant

    Your local AI assistant with infinite memory for code projects.
    """
    pass


@cli.command()
@click.option('--path', default=".", help='Project path')
def index_tasks(path: str):
    """List resumable indexing tasks"""
    # Lazy import
    from acolyte.core.health import ServiceHealthChecker
    from rich.table import Table
    from rich.console import Console

    project_path = Path(path)
    manager = ProjectManager()

    # Check if project is initialized
    if not manager.is_project_initialized(project_path):
        click.echo(click.style("✗ Project not initialized!", fg="red"))
        click.echo("Run 'acolyte init' first")
        sys.exit(1)

    # Load project info and config
    project_info = manager.load_project_info(project_path)
    if not project_info:
        click.echo(click.style("✗ Failed to load project info!", fg="red"))
        sys.exit(1)

    project_id = project_info['project_id']
    project_dir = manager.get_project_dir(project_id)
    config_file = project_dir / ".acolyte"

    if not config_file.exists():
        click.echo(click.style("✗ Project not configured!", fg="red"))
        click.echo("Run 'acolyte install' first")
        sys.exit(1)

    # Load configuration
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        click.echo(click.style(f"✗ Failed to load configuration: {e}", fg="red"))
        sys.exit(1)

    # Check if backend is ready
    health_checker = ServiceHealthChecker(config)
    if not health_checker.wait_for_backend():
        click.echo(click.style("✗ Backend is not ready. Run 'acolyte start' first.", fg="red"))
        sys.exit(1)

    # Get resumable tasks
    try:
        backend_port = config['ports']['backend']
        url = f"http://localhost:{backend_port}/api/index/tasks"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            tasks = response.json().get('tasks', [])

            if not tasks:
                click.echo("No resumable indexing tasks found.")
                return

            # Create table
            console = Console()
            table = Table(title="Resumable Indexing Tasks")

            table.add_column("Task ID", style="cyan")
            table.add_column("Started", style="yellow")
            table.add_column("Progress", style="green")
            table.add_column("Pending Files", style="magenta")
            table.add_column("Last Checkpoint", style="blue")

            for task in tasks:
                progress_pct = (
                    task['processed_files'] / task['total_files'] * 100
                    if task['total_files'] > 0
                    else 0
                )
                progress_str = (
                    f"{task['processed_files']}/{task['total_files']} ({progress_pct:.1f}%)"
                )

                table.add_row(
                    task['task_id'],
                    task.get('started_at', 'Unknown'),
                    progress_str,
                    str(task.get('pending_files', 0)),
                    task.get('last_checkpoint', 'Unknown'),
                )

            console.print(table)
            console.print("\nTo resume a task, use: [cyan]acolyte index --resume TASK_ID[/cyan]")

        else:
            click.echo(click.style(f"✗ Failed to get tasks: {response.text}", fg="red"))
            sys.exit(1)

    except requests.RequestException as e:
        click.echo(click.style(f"✗ Failed to connect to backend: {e}", fg="red"))
        click.echo(click.style("Is the backend running? Try:", fg="yellow"))
        click.echo("  acolyte status")
        click.echo("  acolyte restart")
        click.echo("  acolyte doctor")
        sys.exit(1)


@cli.command()
@click.option(
    '--path',
    default=".",
    callback=validate_project_directory,
    help='Project path (default: current directory)',
)
@click.option('--name', help='Project name (default: directory name)')
@click.option('--force', is_flag=True, help='Force re-initialization')
def init(path: str, name: Optional[str], force: bool):
    """Initialize ACOLYTE in the current project"""
    # Lazy import heavy dependencies
    from acolyte.install.init import ProjectInitializer
    from acolyte.install.common import ACOLYTE_LOGO, animate_text

    project_path = Path(path)
    manager = ProjectManager()

    # Show logo with animation
    print(ACOLYTE_LOGO)
    animate_text(
        click.style("ACOLYTE INIT - Quick Project Setup", fg="cyan", bold=True),
        duration=1.0,
    )
    print("\n")

    click.echo(click.style("🤖 ACOLYTE Project Initialization", fg="cyan", bold=True))
    click.echo(f"Project path: {project_path.resolve()}")

    # Generate project ID
    project_id = manager.get_project_id(project_path)
    click.echo(f"Project ID: {project_id}")

    # Get project name
    if not name:
        name = click.prompt("Project name", default=project_path.name)

    # Get user name
    default_user = os.environ.get('USER', os.environ.get('USERNAME', 'developer'))
    user_name = click.prompt("Your name/username", default=default_user)

    # Create initializer and run
    initializer = ProjectInitializer(project_path, manager.global_dir)

    # The initializer already handles all the initialization logic
    success = initializer.run(project_name=name, user_name=user_name, force=force)

    if success:
        # Project info is saved by init.py to .acolyte.project
        click.echo(click.style("✓ Project initialized successfully!", fg="green"))
        click.echo(f"Configuration stored in: {manager.get_project_dir(project_id)}")
    else:
        click.echo(click.style("✗ Initialization failed!", fg="red"))
        sys.exit(1)


@cli.command()
@click.option('--path', default=".", help='Project path')
@click.option('--repair', is_flag=True, help='Reparar or resume interrupted installation')
def install(path: str, repair: bool):
    """Install and configure ACOLYTE services for the project"""
    # Lazy import heavy dependencies
    from acolyte.install.installer import ProjectInstaller
    from acolyte.install.common import ACOLYTE_LOGO

    # ADVERTENCIA SOBRE EL NOMBRE DEL PAQUETE
    click.echo(click.style("\n⚠️  IMPORTANT ABOUT THE PACKAGE NAME", fg="yellow", bold=True))
    click.echo("The package on PyPI is called 'acolytes' (with 's'), but the command is 'acolyte'.")
    click.echo("If you ran 'pip install acolyte' and it failed, use 'pip install acolytes'.\n")

    project_path = Path(path)
    manager = ProjectManager()

    # Check if project is initialized
    if not manager.is_project_initialized(project_path):
        click.echo(click.style("✗ Project not initialized!", fg="red"))
        click.echo("Run 'acolyte init' first")
        sys.exit(1)

    # Load project info
    project_info = manager.load_project_info(project_path)
    if not project_info:
        click.echo(click.style("✗ Failed to load project info!", fg="red"))
        sys.exit(1)

    project_id = project_info['project_id']
    project_dir = manager.get_project_dir(project_id)

    # Show logo
    print(ACOLYTE_LOGO)
    click.echo(click.style("🔧 ACOLYTE Installation", fg="cyan", bold=True))

    # Mensaje sobre recuperación
    if repair:
        click.echo(
            click.style(
                "[Repair mode] Attempting to resume or repair installation without losing previous progress.",
                fg="yellow",
            )
        )
    else:
        click.echo(
            click.style(
                "If the installation is interrupted, you can resume it with 'acolyte install --repair'",
                fg="yellow",
            )
        )

    # Run installer
    try:
        installer = ProjectInstaller(project_path, manager.global_dir, repair=repair)
        success = asyncio.run(installer.run())

        if success:
            click.echo(click.style("✓ Installation completed successfully!", fg="green"))
            click.echo(f"Configuration saved to: {project_dir}")
        else:
            # User cancelled or installation failed
            # The installer already printed appropriate messages
            sys.exit(0)

    except Exception as e:
        click.echo(click.style(f"✗ Installation error: {e}", fg="red"))
        if os.environ.get('ACOLYTE_DEBUG'):
            import traceback

            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.option('--path', default=".", help='Project path')
def start(path: str):
    """Start ACOLYTE services"""
    # Lazy import for Rich and health checker
    from rich.console import Console
    from rich.progress import (
        Progress,
        SpinnerColumn,
        TextColumn,
        BarColumn,
        TimeElapsedColumn,
        TimeRemainingColumn,
    )
    from acolyte.core.health import ServiceHealthChecker

    project_path = Path(path)
    manager = ProjectManager()

    def _verify_installation(project_dir: Path) -> bool:
        """Verify that installation was completed."""
        # Check for key indicators that install ran successfully
        checks = {
            "Docker compose": project_dir / "infra" / "docker-compose.yml",
            "Database": project_dir / "data" / "acolyte.db",
            "Configuration": project_dir / ".acolyte",
        }

        all_ok = True
        for name, path in checks.items():
            if not path.exists():
                print(f"[red]✗[/red] {name} not found: {path}")
                all_ok = False

        return all_ok

    # Check if project is initialized
    if not manager.is_project_initialized(project_path):
        click.echo(click.style("✗ Project not initialized!", fg="red"))
        click.echo("Run 'acolyte init' first")
        sys.exit(1)

    # Load project info and config
    project_info = manager.load_project_info(project_path)
    if not project_info:
        click.echo(click.style("✗ Failed to load project info!", fg="red"))
        sys.exit(1)

    project_id = project_info['project_id']
    project_dir = manager.get_project_dir(project_id)
    config_file = project_dir / ".acolyte"

    if not config_file.exists():
        click.echo(click.style("✗ Project not configured!", fg="red"))
        click.echo("Run 'acolyte install' first")
        sys.exit(1)

    # Load configuration
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        click.echo(click.style(f"✗ Failed to load configuration: {e}", fg="red"))
        sys.exit(1)

    console = Console()
    # NEW: Check for port conflicts before starting services
    ports = config.get('ports', {})
    port_conflicts = []
    for service, port in ports.items():
        if not PortManager.is_port_available(port):
            port_conflicts.append((service, port))
    if port_conflicts:
        for service, port in port_conflicts:
            owner = get_port_owner(port)
            console.print(
                f"[bold red][ERROR][/bold red] Port {port} is already in use by '{owner}'. The {service.capitalize()} service cannot start."
            )
        console.print(
            "[yellow]Please edit your configuration to use a different port, or run:[/yellow]"
        )
        console.print("    [cyan]acolyte install --repair[/cyan]")
        console.print("to reconfigure ports interactively.")
        sys.exit(1)

    # Start services
    console.print("[bold cyan]🚀 Starting ACOLYTE services...[/bold cyan]")

    if not check_docker_ready():
        console.print("[bold red][ERROR][/bold red] Docker is not available or not running.")
        console.print("[yellow]Please ensure Docker Desktop is installed and running.[/yellow]")
        console.print("If you just started Docker, wait a few seconds and try again.")
        console.print("For help, run: [cyan]acolyte doctor[/cyan]")
        sys.exit(1)

    try:
        docker_cmd = detect_docker_compose_cmd()
        infra_dir = project_dir / "infra"

        if not (infra_dir / "docker-compose.yml").exists():
            console.print("[bold red]✗ Docker configuration not found![/bold red]")
            console.print("Run 'acolyte install' first")
            sys.exit(1)

        # Task 1: Stop existing containers
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            TextColumn("•"),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            task1 = progress.add_task("[yellow]Stopping existing containers...", total=100)
            subprocess.run(
                docker_cmd + ["down", "--remove-orphans"],
                cwd=infra_dir,
                capture_output=True,
                text=True,
                encoding='utf-8',
            )
            progress.update(task1, completed=100)

        # Task 2: Start Docker services
        # First check if images need to be downloaded
        console.print("\n[yellow]Checking Docker images...[/yellow]")

        # Check if images exist
        check_images = subprocess.run(
            ["docker", "images", "-q", "weaviate/weaviate:latest"],
            capture_output=True,
            text=True,
        )

        if not check_images.stdout.strip():
            # Images need to be downloaded
            from rich.panel import Panel

            console.print(
                Panel.fit(
                    "[bold yellow]FIRST TIME SETUP DETECTED[bold yellow]\n\n"
                    "[white]Downloading Docker images. This happens only ONCE.\n"
                    "Subsequent starts will be much faster (≈30s).[/white]",
                    title="[bold cyan]Initial Download[/bold cyan]",
                    border_style="yellow",
                )
            )
            console.print("[dim]• Weaviate vector database (~500MB)[/dim]")
            console.print("[dim]• Backend runtime environment[/dim]")
            console.print("[dim]• Ollama model server[/dim]")
            console.print("[dim]• Qwen2.5-Coder model (~2GB on first run)[/dim]")
            console.print("\n[cyan]☕ This is a good time for a coffee break![/cyan]")
            console.print("[dim]Tip: You'll see Docker's download progress below...[/dim]\n")

            # Run WITHOUT capture_output to show Docker's download progress
            result = subprocess.run(
                docker_cmd + ["up", "-d", "--force-recreate"],
                cwd=infra_dir,
                text=True,
                encoding='utf-8',
            )

            if result.returncode != 0:
                console.print("[bold red]✗ Failed to start services[/bold red]")
                sys.exit(1)

            # Wait for services without progress bar for first time setup
            console.print("\n[yellow]Waiting for services to be ready...[/yellow]")
            health_checker = ServiceHealthChecker(config)

            # Simple status messages for first time
            console.print("[dim]• Checking Weaviate...[/dim]")
            for i in range(120):
                if health_checker._check_service_once(
                    "Weaviate", config['ports']['weaviate'], "/v1/.well-known/ready"
                ):
                    console.print("[green]✓[/green] Weaviate is ready")
                    break
                time.sleep(1)
            else:
                console.print("[bold red]✗ Weaviate failed to start[/bold red]")
                sys.exit(1)

            # Check if Ollama is ready first
            console.print("[dim]• Checking Ollama...[/dim]")
            ollama_ready = False
            for i in range(120):
                try:
                    ollama_check = subprocess.run(
                        ["docker", "exec", "acolyte-ollama", "ollama", "list"],
                        capture_output=True,
                        text=True,
                    )
                    if ollama_check.returncode == 0:
                        console.print("[green]✓[/green] Ollama is ready")
                        ollama_ready = True
                        break
                except (subprocess.SubprocessError, FileNotFoundError, OSError):
                    pass
                time.sleep(1)
            else:
                console.print("[bold red]✗ Ollama failed to start[/bold red]")
                sys.exit(1)

            # CRITICAL: Preload the model to avoid timeout issues
            if ollama_ready:
                console.print("[dim]• Preloading Ollama model...[/dim]")
                preload_result = subprocess.run(
                    ["docker", "exec", "acolyte-ollama", "ollama", "run", "acolyte:latest", "test"],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    timeout=300,  # 5 minutes timeout for first load
                )
                if preload_result.returncode == 0:
                    console.print("[green]✓[/green] Model preloaded successfully")
                else:
                    console.print("[yellow]⚠[/yellow] Model preload failed, but continuing...")

            # Create the acolyte model if it doesn't exist
            if ollama_ready:
                console.print("[dim]• Checking for acolyte model...[/dim]")
                if not ensure_acolyte_model_exists(config, infra_dir, console):
                    console.print("[bold red]✗ Failed to create acolyte model[/bold red]")
                    console.print(
                        "[yellow]Continuing anyway - backend will use base model[/yellow]"
                    )

            console.print("[dim]• Checking Backend API...[/dim]")

            class FancySpinner(SpinnerColumn):
                spinners = ["🤖", "⚡", "🔥", "💡", "🤖", "⚡", "🔥", "💡"]

                def render(self, task):
                    frame = int(time.time() * 4) % len(self.spinners)
                    return self.spinners[frame]

            with Progress(
                FancySpinner(style="bold magenta"),
                TextColumn(
                    "[bold yellow]🤖 Warming up AI model...[/bold yellow] [dim](first response may take 30-60s)[/dim]"
                ),
                console=console,
            ) as progress:
                task = progress.add_task("[cyan]Waiting for Backend API...", total=None)
                for i in range(120):
                    if health_checker._check_service_once(
                        "Backend", config['ports']['backend'], "/api/health"
                    ):
                        progress.update(task, completed=1)
                        break
                    time.sleep(1)
                else:
                    progress.stop()
                    console.print("[bold red]✗ Backend failed to start[/bold red]")
                    sys.exit(1)

        else:
            # Images already exist, use progress bar
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
                TextColumn("•"),
                TimeRemainingColumn(),
                console=console,
            ) as progress:
                task2 = progress.add_task("[cyan]Starting Docker containers...", total=100)
                result = subprocess.run(
                    docker_cmd + ["up", "-d", "--force-recreate"],
                    cwd=infra_dir,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                )
                progress.update(task2, completed=100)

                if result.returncode != 0:
                    console.print("[bold red]✗ Failed to start services[/bold red]")
                    if hasattr(result, 'stderr'):
                        console.print(f"[red]Error: {result.stderr}[/red]")
                    sys.exit(1)

                # Task 3: Wait for services
                health_checker = ServiceHealthChecker(config)

                # Weaviate
                task3 = progress.add_task("[green]Waiting for Weaviate...", total=120)
                for i in range(120):
                    if health_checker._check_service_once(
                        "Weaviate", config['ports']['weaviate'], "/v1/.well-known/ready"
                    ):
                        progress.update(task3, completed=120)
                        break
                    progress.update(task3, advance=1)
                    time.sleep(1)
                else:
                    console.print("[bold red]✗ Weaviate failed to start[/bold red]")
                    # Show last 5 log lines from weaviate
                    try:
                        logs = subprocess.check_output(
                            docker_cmd + ["logs", "--tail", "5", "weaviate"], cwd=infra_dir
                        ).decode(errors="replace")
                        console.print("[yellow]Last 5 log lines from Weaviate:[/yellow]")
                        console.print(logs)
                    except Exception as e:
                        console.print(f"[red]Could not fetch Weaviate logs: {e}[/red]")
                    sys.exit(1)

                # Ollama model check and creation
                task_ollama = progress.add_task("[green]Checking Ollama model...", total=100)

                # Use the centralized function to ensure model exists
                if ensure_acolyte_model_exists(config, infra_dir, console):
                    progress.update(task_ollama, completed=100, description="[green]Model ready")
                else:
                    progress.update(
                        task_ollama, completed=100, description="[yellow]Model creation failed"
                    )
                    console.print(
                        "[yellow]Continuing anyway - backend will use base model[/yellow]"
                    )

                # CRITICAL: Preload the model to avoid timeout issues
                task_preload = progress.add_task(
                    "[cyan]Preloading model (prevents timeouts)...", total=100
                )
                preload_result = subprocess.run(
                    ["docker", "exec", "acolyte-ollama", "ollama", "run", "acolyte:latest", "test"],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    timeout=300,  # 5 minutes timeout
                )
                if preload_result.returncode == 0:
                    progress.update(
                        task_preload, completed=100, description="[green]Model preloaded"
                    )
                else:
                    progress.update(
                        task_preload, completed=100, description="[yellow]Preload failed"
                    )

                # Backend
                task4 = progress.add_task("[green]Waiting for Backend API...", total=120)
                for i in range(120):
                    if health_checker._check_service_once(
                        "Backend", config['ports']['backend'], "/api/health"
                    ):
                        progress.update(task4, completed=120)
                        break
                    progress.update(task4, advance=1)
                    time.sleep(1)
                else:
                    console.print("[bold red]✗ Backend failed to start[/bold red]")
                    # Show last 5 log lines from backend
                    try:
                        logs = subprocess.check_output(
                            docker_cmd + ["logs", "--tail", "5", "backend"], cwd=infra_dir
                        ).decode(errors="replace")
                        console.print("[yellow]Last 5 log lines from Backend:[/yellow]")
                        console.print(logs)
                    except Exception as e:
                        console.print(f"[red]Could not fetch Backend logs: {e}[/red]")
                    sys.exit(1)

        console.print("[bold green]✓ All services are ready![/bold green]")
        console.print(f"\n[dim]Backend API: http://localhost:{config['ports']['backend']}[/dim]")
        console.print(f"[dim]Weaviate: http://localhost:{config['ports']['weaviate']}[/dim]")
        console.print(f"[dim]Ollama: http://localhost:{config['ports']['ollama']}[/dim]")
        console.print(
            "\n[bold cyan]ACOLYTE is ready! Use 'acolyte status' to check services.[/bold cyan]"
        )

    except Exception as e:
        click.echo(click.style(f"✗ Error starting services: {e}", fg="red"))
        sys.exit(1)


@cli.command()
@click.option('--path', default=".", help='Project path')
def stop(path: str):
    """Stop ACOLYTE services"""
    project_path = Path(path)
    manager = ProjectManager()

    # Check if project is initialized
    if not manager.is_project_initialized(project_path):
        click.echo(click.style("✗ Project not initialized!", fg="red"))
        sys.exit(1)

    # Load project info
    project_info = manager.load_project_info(project_path)
    if not project_info:
        click.echo(click.style("✗ Failed to load project info!", fg="red"))
        sys.exit(1)

    project_id = project_info['project_id']
    project_dir = manager.get_project_dir(project_id)
    infra_dir = project_dir / "infra"

    if not (infra_dir / "docker-compose.yml").exists():
        click.echo(click.style("✗ Docker configuration not found!", fg="red"))
        sys.exit(1)

    # Stop services
    click.echo(click.style("🛑 Stopping ACOLYTE services...", fg="cyan"))

    try:
        docker_cmd = detect_docker_compose_cmd()
        result = subprocess.run(
            docker_cmd + ["down"],
            cwd=infra_dir,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            click.echo(click.style(f"✗ Failed to stop services: {result.stderr}", fg="red"))
            sys.exit(1)

        click.echo(click.style("✓ Services stopped successfully!", fg="green"))

    except Exception as e:
        click.echo(click.style(f"✗ Error stopping services: {e}", fg="red"))
        sys.exit(1)


@cli.command()
@click.option('--path', default=".", help='Project path')
def status(path: str):
    """Check ACOLYTE status for the project"""
    project_path = Path(path)
    manager = ProjectManager()

    # Check if project is initialized
    if not manager.is_project_initialized(project_path):
        click.echo(click.style("✗ Project not initialized!", fg="red"))
        click.echo("Run 'acolyte init' first")
        sys.exit(1)

    # Load project info
    project_info = manager.load_project_info(project_path)
    if not project_info:
        click.echo(click.style("✗ Failed to load project info!", fg="red"))
        sys.exit(1)

    project_id = project_info['project_id']
    project_dir = manager.get_project_dir(project_id)
    config_file = project_dir / ".acolyte"

    click.echo(click.style("📊 ACOLYTE Status", fg="cyan", bold=True))
    click.echo(f"Project: {project_info.get('name', 'Unknown')}")
    click.echo(f"Project ID: {project_id}")
    click.echo(f"Path: {project_path.resolve()}")

    # Check configuration
    if config_file.exists():
        click.echo(click.style("✓ Configuration: Found", fg="green"))
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            ports = config.get('ports', {})
            click.echo(f"  Backend: localhost:{ports.get('backend', 'N/A')}")
            click.echo(f"  Weaviate: localhost:{ports.get('weaviate', 'N/A')}")
            click.echo(f"  Ollama: localhost:{ports.get('ollama', 'N/A')}")
        except Exception:
            click.echo(click.style("⚠ Configuration: Invalid", fg="yellow"))
    else:
        click.echo(click.style("✗ Configuration: Not found", fg="red"))
        click.echo("  Run 'acolyte install' to configure")

    # Check Docker services
    infra_dir = project_dir / "infra"
    if (infra_dir / "docker-compose.yml").exists():
        click.echo(click.style("✓ Docker: Configured", fg="green"))

        try:
            docker_cmd = detect_docker_compose_cmd()
            result = subprocess.run(
                docker_cmd + ["ps"],
                cwd=infra_dir,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:  # Has services
                    click.echo("  Services:")
                    for line in lines[1:]:  # Skip header
                        if line.strip():
                            click.echo(f"    {line.strip()}")
                else:
                    click.echo("  No services running")
            else:
                click.echo(click.style("⚠ Docker: Error checking status", fg="yellow"))

        except Exception:
            click.echo(click.style("⚠ Docker: Error checking status", fg="yellow"))
    else:
        click.echo(click.style("✗ Docker: Not configured", fg="red"))


@cli.command()
@click.option('--path', default=".", help='Project path')
@click.option('--partial', is_flag=True, help='Partial project indexing (incremental)')
@click.option('--progress/--no-progress', default=True, help='Show live progress')
@click.option('--verbose', is_flag=True, help='Show detailed progress')
@click.option('--resume', help='Resume previous indexing task by ID')
def index(path: str, partial: bool, progress: bool, verbose: bool, resume: Optional[str]):
    """Index project files (full index by default)"""
    # Import the real implementation
    from acolyte.install.commands.index import index_impl

    # Create manager and call implementation
    manager = ProjectManager()
    return index_impl(path, partial, progress, verbose, resume, manager)


@cli.command()
def projects():
    """List all ACOLYTE projects"""
    manager = ProjectManager()

    click.echo(click.style("📁 ACOLYTE Projects", fg="cyan", bold=True))

    if not manager.projects_dir.exists():
        click.echo("No projects found")
        return

    projects_found = False
    for project_dir in manager.projects_dir.iterdir():
        if project_dir.is_dir():
            projects_found = True
            project_id = project_dir.name

            # Try to load project info
            config_file = project_dir / ".acolyte"
            project_name = "Unknown"
            project_path = "Unknown"

            if config_file.exists():
                try:
                    with open(config_file, 'r') as f:
                        config = yaml.safe_load(f)
                    project_name = config.get('project', {}).get('name', 'Unknown')
                    # Don't use the relative path from config
                    # project_path = config.get('project', {}).get('path', 'Unknown')
                except Exception:
                    pass

            # Try to find the real project path by searching for .acolyte.project files
            # that contain this project_id
            real_project_path = None

            # First check common locations
            home = Path.home()
            common_dirs = [
                home / "Desktop",
                home / "Documents",
                home / "Projects",
                home / "repos",
                home / "dev",
                home / "workspace",
                home / "code",
                home,
            ]

            for base_dir in common_dirs:
                if base_dir.exists():
                    try:
                        # Search for .acolyte.project files
                        for acolyte_project_file in base_dir.rglob(".acolyte.project"):
                            try:
                                with open(acolyte_project_file) as f:
                                    project_data = yaml.safe_load(f)
                                    if project_data.get('project_id') == project_id:
                                        # Found it!
                                        real_project_path = project_data.get('project_path')
                                        if not real_project_path:
                                            # Fallback to parent directory of .acolyte.project
                                            real_project_path = str(acolyte_project_file.parent)
                                        break
                            except Exception:
                                continue

                        if real_project_path:
                            break
                    except Exception:
                        continue

            if real_project_path:
                project_path = real_project_path
            elif config_file.exists():
                # Fallback to showing relative path from config
                try:
                    with open(config_file, 'r') as f:
                        config = yaml.safe_load(f)
                    project_path = config.get('project', {}).get('path', 'Unknown')
                except Exception:
                    pass

            click.echo(f"\nProject ID: {project_id}")
            click.echo(f"Name: {project_name}")
            click.echo(f"Path: {project_path}")

            # Check if services are running
            try:
                docker_cmd = detect_docker_compose_cmd()
                result = subprocess.run(
                    docker_cmd + ["ps", "--quiet"],
                    cwd=project_dir / "infra",
                    capture_output=True,
                    text=True,
                )

                if result.returncode == 0 and result.stdout.strip():
                    click.echo(click.style("Status: Running", fg="green"))
                else:
                    click.echo(click.style("Status: Stopped", fg="yellow"))
            except Exception:
                click.echo(click.style("Status: Unknown", fg="yellow"))

    if not projects_found:
        click.echo("No projects found")


@cli.command()
@click.option('--path', default=".", help='Project path')
def clean(path: str):
    """Clean ACOLYTE cache and temporary files"""
    project_path = Path(path)
    manager = ProjectManager()

    # Check if project is initialized
    if not manager.is_project_initialized(project_path):
        click.echo(click.style("✗ Project not initialized!", fg="red"))
        sys.exit(1)

    # Load project info
    project_info = manager.load_project_info(project_path)
    if not project_info:
        click.echo(click.style("✗ Failed to load project info!", fg="red"))
        sys.exit(1)

    project_id = project_info['project_id']
    project_dir = manager.get_project_dir(project_id)

    click.echo(click.style("🧹 Cleaning ACOLYTE cache...", fg="cyan"))

    # Clean cache directories
    cache_dirs = [
        project_dir / "data" / "embeddings_cache",
        project_dir / "data" / "logs",
    ]

    cleaned = 0
    for cache_dir in cache_dirs:
        if cache_dir.exists():
            try:
                shutil.rmtree(cache_dir)
                cache_dir.mkdir(parents=True, exist_ok=True)
                click.echo(f"✓ Cleaned: {cache_dir.name}")
                cleaned += 1
            except Exception as e:
                click.echo(click.style(f"⚠ Failed to clean {cache_dir.name}: {e}", fg="yellow"))

    if cleaned > 0:
        click.echo(click.style(f"✓ Cleaned {cleaned} cache directories", fg="green"))
    else:
        click.echo("No cache directories found to clean")


# Import the logs command from console module
# The implementation has been moved to console/logs_command.py for better organization
cli.add_command(logs)


@cli.command()
@click.option('--path', default=".", help='Project path')
@click.option('--force', is_flag=True, help='Force reset without confirmation')
def reset(path: str, force: bool):
    """Reset ACOLYTE installation for this project"""
    project_path = Path(path)
    manager = ProjectManager()

    # Check if project is initialized
    if not manager.is_project_initialized(project_path):
        click.echo(click.style("✗ Project not initialized!", fg="red"))
        sys.exit(1)

    # Load project info
    project_info = manager.load_project_info(project_path)
    if not project_info:
        click.echo(click.style("✗ Failed to load project info!", fg="red"))
        sys.exit(1)

    project_id = project_info['project_id']
    project_dir = manager.get_project_dir(project_id)

    click.echo(click.style("🔄 ACOLYTE Project Reset", fg="cyan", bold=True))
    click.echo(f"Project: {project_info.get('name', 'Unknown')}")
    click.echo(f"Project ID: {project_id}")
    click.echo(f"Reset directory: {project_dir}")

    if not force:
        if not click.confirm("This will delete all ACOLYTE data for this project. Continue?"):
            click.echo("Reset cancelled.")
            return

    try:
        # Stop services if running
        infra_dir = project_dir / "infra"
        if (infra_dir / "docker-compose.yml").exists():
            click.echo("Stopping services...")
            try:
                docker_cmd = detect_docker_compose_cmd()
                # Force stop with timeout
                result = subprocess.run(
                    docker_cmd + ["down", "--timeout", "30"],
                    cwd=infra_dir,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                if result.returncode == 0:
                    click.echo("✓ Services stopped")
                else:
                    click.echo("⚠️  Some services may still be running")

                # Wait a bit for file handles to be released
                import time

                time.sleep(3)

            except subprocess.TimeoutExpired:
                click.echo("⚠️  Services stop timed out, trying to force stop...")
                try:
                    if docker_cmd:  # Check if docker_cmd is not None
                        subprocess.run(
                            docker_cmd + ["down", "--volumes", "--remove-orphans"],
                            cwd=infra_dir,
                            capture_output=True,
                            text=True,
                            timeout=30,
                        )
                        time.sleep(2)
                except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
                    pass
            except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
                pass  # Ignore errors if services not running

        # Try to remove project directory with retry logic
        if project_dir.exists():
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    shutil.rmtree(project_dir)
                    click.echo("✓ Project data removed")
                    break
                except PermissionError:
                    if attempt < max_retries - 1:
                        click.echo(
                            f"⚠️  Retry {attempt + 1}/{max_retries}: Waiting for files to be released..."
                        )
                        time.sleep(2)
                    else:
                        click.echo("⚠️  Some files could not be removed (may be in use)")
                        click.echo("   You may need to restart your terminal or computer")
                        # Try to remove individual files that might be locked
                        try:
                            for root, dirs, files in os.walk(project_dir, topdown=False):
                                for file in files:
                                    try:
                                        os.remove(os.path.join(root, file))
                                    except (PermissionError, FileNotFoundError, OSError):
                                        pass
                                for dir in dirs:
                                    try:
                                        os.rmdir(os.path.join(root, dir))
                                    except (PermissionError, FileNotFoundError, OSError):
                                        pass
                            click.echo("✓ Partial cleanup completed")
                        except (PermissionError, FileNotFoundError, OSError):
                            pass
                except Exception as e:
                    click.echo(f"✗ Error removing project directory: {e}")
                    break

        # Remove project marker and any init logs
        project_file = project_path / ".acolyte.project"
        if project_file.exists():
            project_file.unlink()
            click.echo("✓ Project marker removed")

        # Remove any init log files that might have been created in the past
        init_log_file = project_path / ".acolyte.init.log"
        if init_log_file.exists():
            try:
                init_log_file.unlink()
                click.echo("✓ Old init log file removed")
            except (PermissionError, FileNotFoundError, OSError):
                pass  # Ignore if can't remove

        click.echo(click.style("✅ Project reset completed!", fg="green"))
        click.echo("Run 'acolyte init' to reinitialize the project")

    except Exception as e:
        click.echo(click.style(f"✗ Reset failed: {e}", fg="red"))
        sys.exit(1)


@cli.command()
@click.option('--fix', is_flag=True, help='Attempt to fix issues automatically')
@click.option('--project', default=".", help='Project path to diagnose')
@click.option('--clean-sqlite', is_flag=True, help='Clean SQLite database locks and orphaned files')
def doctor(fix: bool, project: str, clean_sqlite: bool):
    """Diagnose and fix common ACOLYTE issues

    Run comprehensive diagnostics on your ACOLYTE installation:
    - System requirements (Docker, Python, disk space)
    - Project configuration and installation state
    - Running services health checks
    - Common error patterns in logs

    Use --fix to attempt automatic repairs.
    Use --clean-sqlite to clean database locks and orphaned files.
    """
    # Import the advanced doctor implementation
    from acolyte.install.commands.doctor import run_doctor

    # Run the comprehensive diagnostics
    run_doctor(fix=fix, project=project, clean_sqlite=clean_sqlite)


# Progress monitoring moved to cli/commands/progress_monitor.py


# Legacy monitor moved to cli/commands/progress_monitor.py


# Polling monitor moved to cli/commands/progress_monitor.py


def get_port_owner(port: int) -> str:
    """Get the process using a port (cross-platform, best effort)."""
    try:
        if sys.platform == "win32":
            # Windows: netstat -ano | findstr :port
            result = subprocess.run(["netstat", "-ano"], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if f":{port}" in line and "LISTENING" in line:
                    pid = line.split()[-1]
                    # Get process name from PID
                    proc_result = subprocess.run(
                        ["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True
                    )
                    for proc_line in proc_result.stdout.splitlines():
                        if pid in proc_line:
                            parts = proc_line.split()
                            if parts:
                                return f"{parts[0]} (PID: {pid})"
                    return f"PID {pid}"
        else:
            # Linux/Mac: lsof -i :port
            result = subprocess.run(["lsof", "-i", f":{port}"], capture_output=True, text=True)
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    parts = lines[1].split()
                    if len(parts) >= 2:
                        return f"{parts[0]} (PID: {parts[1]})"
    except Exception:
        pass
    return "unknown process"


@cli.command()
@click.option(
    '--rebuild-config', is_flag=True, help='Rebuild .acolyte configuration from detected state'
)
def repair(rebuild_config: bool):
    """Repair project configuration or state."""
    if rebuild_config:
        import re
        from pathlib import Path
        import yaml
        from typing import Any, Dict

        project_path = Path('.')
        config_file = project_path / '.acolyte'
        config: Dict[str, Any] = {
            'project': {
                'name': project_path.name,
                'path': str(project_path.resolve()),
            }
        }
        # Detect model from Modelfile
        modelfile_path = project_path / 'Modelfile'
        if modelfile_path.exists():
            import yaml

            try:
                with open(modelfile_path, 'r') as f:
                    for line in f:
                        if 'FROM' in line:
                            model_name = line.split('FROM')[-1].strip()
                            config['model'] = {'name': model_name}
                            break
            except (FileNotFoundError, yaml.YAMLError, UnicodeDecodeError) as e:
                click.echo(click.style(f"Warning: Could not parse Modelfile: {e}", fg="yellow"))
        # Recover ports from docker-compose.yml
        compose_path = project_path / 'infra' / 'docker-compose.yml'
        if compose_path.exists():
            import yaml as yamllib

            try:
                with open(compose_path, 'r') as f:
                    compose = yamllib.safe_load(f)
                ports = {}
                for service in ['weaviate', 'ollama', 'backend']:
                    svc = compose.get('services', {}).get(service, {})
                    if 'ports' in svc and svc['ports']:
                        # Get the first port mapping
                        port_map = svc['ports'][0]
                        match = re.match(r"(\d+):", port_map)
                        if match:
                            ports[service] = int(match.group(1))
                if ports:
                    config['ports'] = ports
            except (FileNotFoundError, yamllib.YAMLError, KeyError) as e:
                click.echo(
                    click.style(f"Warning: Could not parse docker-compose.yml: {e}", fg="yellow")
                )
        # Infer stack from project files
        stack = []
        if (project_path / 'package.json').exists():
            stack.append('nodejs')
        if (project_path / 'pyproject.toml').exists():
            stack.append('python')
        if (project_path / 'go.mod').exists():
            stack.append('go')
        if (project_path / 'requirements.txt').exists():
            stack.append('python')
        if (project_path / 'pom.xml').exists():
            stack.append('java')
        if stack:
            config['stack'] = sorted(set(stack))
        with open(config_file, 'w') as f:
            yaml.safe_dump(config, f)
        click.echo(
            click.style('Rebuilt .acolyte configuration file from detected state.', fg='green')
        )
        if 'model' in config:
            click.echo(click.style(f"Detected model: {config['model']['name']}", fg='cyan'))
        if 'ports' in config:
            click.echo(click.style(f"Detected ports: {config['ports']}", fg='cyan'))
        if 'stack' in config:
            click.echo(click.style(f"Detected stack: {config['stack']}", fg='cyan'))
    else:
        click.echo(
            click.style(
                'No repair action specified. Use --rebuild-config to rebuild .acolyte.', fg='yellow'
            )
        )


def main():
    """Main entry point"""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        click.echo(click.style(f"Error: {e}", fg="red"))
        if os.environ.get('ACOLYTE_DEBUG'):
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
