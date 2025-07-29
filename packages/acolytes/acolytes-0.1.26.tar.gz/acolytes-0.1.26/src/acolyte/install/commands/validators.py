"""Validators for index command."""

import click
import yaml
from pathlib import Path
from typing import Dict, Any

from acolyte.core.health import ServiceHealthChecker
from acolyte.install.database import DatabaseInitializer


def validate_project_initialized(project_path: Path, manager) -> None:
    """Check if project is initialized."""
    if not manager.is_project_initialized(project_path):
        click.echo(click.style("✗ Project not initialized!", fg="red"))
        click.echo("Run 'acolyte init' first")
        raise SystemExit(1)


def validate_project_info(project_path: Path, manager) -> Dict[str, Any]:
    """Load and validate project info."""
    project_info = manager.load_project_info(project_path)
    if not project_info:
        click.echo(click.style("✗ Failed to load project info!", fg="red"))
        raise SystemExit(1)
    return project_info


def validate_project_configured(project_dir: Path) -> Dict[str, Any]:
    """Check if project is configured and load config."""
    config_file = project_dir / ".acolyte"

    if not config_file.exists():
        click.echo(click.style("✗ Project not configured!", fg="red"))
        click.echo("Run 'acolyte install' first")
        raise SystemExit(1)

    # Load configuration
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        click.echo(click.style(f"✗ Failed to load configuration: {e}", fg="red"))
        raise SystemExit(1)


def validate_backend_ready(config: Dict[str, Any]) -> None:
    """Check if backend is ready."""
    health_checker = ServiceHealthChecker(config)
    if not health_checker.wait_for_backend():
        click.echo(click.style("✗ Backend is not ready. Run 'acolyte start' first.", fg="red"))
        raise SystemExit(1)


def validate_version_compatibility(project_path: Path, project_id: str, global_dir: Path) -> None:
    """Check version compatibility before indexing."""
    try:
        dbi = DatabaseInitializer(
            project_path=project_path, project_id=project_id, global_dir=global_dir
        )
        import asyncio

        asyncio.run(dbi.check_version_compatibility())
    except SystemExit:
        click.echo(
            click.style(
                "✗ Version incompatibility detected. Run 'acolyte migrate' or reindex your project.",
                fg="red",
            )
        )
        raise SystemExit(1)
    except Exception as e:
        click.echo(click.style(f"✗ Failed to check version compatibility: {e}", fg="red"))
        raise SystemExit(1)
