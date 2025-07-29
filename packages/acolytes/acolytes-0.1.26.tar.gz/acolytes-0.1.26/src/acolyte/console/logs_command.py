"""
ACOLYTE logs command implementation.
Handles viewing and formatting of service logs.
"""

import subprocess
import sys
import os
from pathlib import Path
from typing import Optional

import click

from .logs_formatter import colorize_log_line

# Enable color support on Windows
if sys.platform == 'win32':
    # Force color output
    os.environ['FORCE_COLOR'] = '1'

    # Try to enable ANSI escape sequences on Windows console
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        # Enable ANSI escape sequences
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass  # Ignore if it fails


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


@click.command()
@click.option('--path', default=".", help='Project path')
@click.option('-f', '--follow', is_flag=True, help='Follow log output (like tail -f)')
@click.option('-n', '--lines', default=100, help='Number of lines to show (default: 100)')
@click.option(
    '-s',
    '--service',
    type=click.Choice(['backend', 'weaviate', 'ollama', 'all']),
    default='all',
    help='Service to show logs for',
)
@click.option('--file', is_flag=True, help='Show project log file instead of Docker logs')
@click.option('-g', '--grep', help='Filter logs containing text')
@click.option(
    '--level',
    type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR']),
    help='Filter by log level (only for --file)',
)
def logs(
    path: str,
    follow: bool,
    lines: int,
    service: str,
    file: bool,
    grep: Optional[str],
    level: Optional[str],
):
    """View ACOLYTE service logs"""
    # Import here to avoid circular imports
    from acolyte.cli import ProjectManager

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

    if file:
        # Show log file with colorization
        show_file_logs(
            project_dir=project_dir,
            project_id=project_id,
            lines=lines,
            grep=grep,
            level=level,
            follow=follow,
        )
    else:
        # Show Docker logs
        show_docker_logs(
            project_dir=project_dir, service=service, lines=lines, follow=follow, grep=grep
        )


def show_file_logs(
    project_dir: Path,
    project_id: str,
    lines: int,
    grep: Optional[str],
    level: Optional[str],
    follow: bool,
) -> None:
    """Show and colorize log file contents."""
    log_file = project_dir / "data" / "logs" / f"{project_id}.log"

    if not log_file.exists():
        click.echo(click.style("✗ Log file not found!", fg="red"))
        click.echo(f"Expected location: {log_file}")
        sys.exit(1)

    if follow:
        # Follow mode - like tail -f
        show_file_logs_follow(log_file, grep, level)
    else:
        # Normal mode - show last N lines
        try:
            with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
                log_lines = f.readlines()

            # Apply filters
            filtered_lines = []
            for line in log_lines:
                # Skip empty lines
                if not line.strip():
                    continue

                # Apply level filter
                if level and level not in line:
                    continue

                # Apply grep filter
                if grep and grep not in line:
                    continue

                filtered_lines.append(line)

            # Show last N lines
            filtered_lines = filtered_lines[-lines:]

            # Colorize and display
            for line in filtered_lines:
                colorized = colorize_log_line(line.rstrip())
                # Force color output
                click.echo(colorized, color=True)

        except Exception as e:
            click.echo(click.style(f"✗ Error reading log file: {e}", fg="red"))
            sys.exit(1)


def show_file_logs_follow(log_file: Path, grep: Optional[str], level: Optional[str]) -> None:
    """Follow log file in real-time with colorization."""
    import time

    try:
        with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
            # Go to end of file
            f.seek(0, 2)

            while True:
                line = f.readline()
                if line:
                    # Apply filters
                    if level and level not in line:
                        continue
                    if grep and grep not in line:
                        continue

                    # Colorize and display
                    colorized = colorize_log_line(line.rstrip())
                    # Force color output
                    click.echo(colorized, color=True)
                else:
                    time.sleep(0.1)  # Small delay to avoid busy waiting

    except KeyboardInterrupt:
        click.echo("\nLog following stopped.")
    except Exception as e:
        click.echo(click.style(f"✗ Error following log file: {e}", fg="red"))
        sys.exit(1)


def show_docker_logs(
    project_dir: Path, service: str, lines: int, follow: bool, grep: Optional[str]
) -> None:
    """Show Docker container logs."""
    infra_dir = project_dir / "infra"

    if not (infra_dir / "docker-compose.yml").exists():
        click.echo(click.style("✗ Docker configuration not found!", fg="red"))
        click.echo("Run 'acolyte install' first")
        sys.exit(1)

    try:
        docker_cmd = detect_docker_compose_cmd()

        if service == 'all':
            cmd = docker_cmd + ["logs", "--tail", str(lines)]
            if follow:
                cmd.append("-f")
        else:
            cmd = docker_cmd + ["logs", "--tail", str(lines), service]
            if follow:
                cmd.append("-f")

        # Run docker logs
        process = subprocess.Popen(
            cmd,
            cwd=infra_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace',
            bufsize=1,
            universal_newlines=True,
        )

        # Stream output with optional colorization
        if process.stdout:
            for line in process.stdout:
                if grep is None or grep in line:
                    # For docker logs, we could also colorize if desired
                    # For now, just echo as-is
                    click.echo(line.rstrip())

        process.wait()

    except KeyboardInterrupt:
        click.echo("\nLog streaming stopped.")
    except Exception as e:
        click.echo(click.style(f"✗ Error showing logs: {e}", fg="red"))
        sys.exit(1)
