"""Progress monitoring for indexing."""

import asyncio
import time
import os
from typing import Dict, Any, Union

from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    MofNCompleteColumn,
)
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.layout import Layout

from acolyte.core.progress import ProgressMonitor


async def monitor_indexing_progress(
    backend_port: int, websocket_path: str, task_id: str, total_files: int, verbose: bool = False
):
    """Monitor indexing progress via WebSocket with Rich progress bar."""
    console = Console()

    # Crear layout profesional
    layout = Layout()

    # Dividir la pantalla en secciones
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="progress", size=8),
        Layout(name="stats", size=6),
        Layout(name="footer", size=3),
    )

    # Header profesional
    header = Panel(
        Text("🚀 ACOLYTE Indexing Progress", style="bold cyan", justify="center"),
        style="blue",
        border_style="bright_blue",
    )
    layout["header"].update(header)

    # Footer con información del task
    footer = Panel(
        Text(f"Task ID: {task_id} | Backend: localhost:{backend_port}", style="dim"),
        style="black on white",
        border_style="bright_black",
    )
    layout["footer"].update(footer)

    # Crear progress con múltiples barras
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Processing:", style="bold blue"),
        BarColumn(bar_width=40),
        MofNCompleteColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
        expand=True,
    )

    # Crear tabla de estadísticas
    stats_table = Table(
        title="📊 Indexing Statistics", show_header=True, header_style="bold magenta"
    )
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="green")

    # Inicializar estadísticas con tipos explícitos
    stats: Dict[str, Union[int, float, str]] = {
        "files_processed": 0,
        "chunks_created": 0,
        "embeddings_generated": 0,
        "files_skipped": 0,
        "errors": 0,
        "current_file": "Starting...",
        "files_per_second": 0.0,
        "chunks_per_file": 0.0,
    }

    def update_stats_table():
        """Actualizar tabla de estadísticas"""
        # Crear nueva tabla cada vez (Rich Table no tiene clear)
        new_table = Table(
            title="📊 Indexing Statistics", show_header=True, header_style="bold magenta"
        )
        new_table.add_column("Metric", style="cyan")
        new_table.add_column("Value", style="green")

        new_table.add_row("Files Processed", f"{stats['files_processed']}")
        new_table.add_row("Chunks Created", f"{stats['chunks_created']}")
        new_table.add_row("Embeddings Generated", f"{stats['embeddings_generated']}")
        new_table.add_row("Files Skipped", f"{stats['files_skipped']}")
        new_table.add_row(
            "Errors", f"[red]{stats['errors']}[/red]" if int(stats['errors']) > 0 else "0"
        )
        new_table.add_row("Files/Second", f"{stats['files_per_second']:.2f}")
        new_table.add_row("Chunks/File", f"{stats['chunks_per_file']:.1f}")
        new_table.add_row("Current File", f"[yellow]{stats['current_file']}[/yellow]")

        return new_table

    # Inicializar task de progreso
    with progress:
        main_task = progress.add_task("[cyan]Indexing files...", total=total_files, completed=0)

        # Configurar layouts
        layout["progress"].update(progress)
        layout["stats"].update(update_stats_table())

        # Usar Live para actualización en tiempo real
        with Live(layout, refresh_per_second=4, console=console) as live:
            start_time = time.time()

            try:
                # Usar el monitor unificado
                monitor = ProgressMonitor(backend_port, console)

                # Función para actualizar la UI
                async def update_ui(event_data: Dict[str, Any]):
                    """Actualizar UI con datos del evento"""
                    # Cast explícito para evitar errores de mypy
                    stats["files_processed"] = int(event_data.get("current", 0))
                    stats["chunks_created"] = int(event_data.get("chunks_created", 0))
                    stats["embeddings_generated"] = int(event_data.get("embeddings_generated", 0))
                    stats["files_skipped"] = int(event_data.get("files_skipped", 0))
                    stats["errors"] = int(event_data.get("errors", 0))
                    stats["current_file"] = str(event_data.get("current_file", "Processing..."))

                    # Calcular velocidad
                    elapsed = time.time() - start_time
                    if elapsed > 0:
                        stats["files_per_second"] = float(stats["files_processed"]) / elapsed

                    # Calcular chunks por archivo
                    files_processed = int(stats["files_processed"])
                    if files_processed > 0:
                        stats["chunks_per_file"] = float(stats["chunks_created"]) / files_processed

                    # Actualizar barra de progreso
                    progress.update(
                        main_task,
                        completed=float(stats["files_processed"]),
                        total=int(event_data.get("total", total_files)),
                        description=f"[cyan]Processing: {os.path.basename(str(stats['current_file']))}",
                    )

                    # Actualizar tabla de estadísticas
                    layout["stats"].update(update_stats_table())

                    # Actualizar live display
                    live.update(layout)

                # Monitorear usando el método existente
                # Como no podemos usar callback personalizado, usaremos el método básico
                # y mostraremos las estadísticas finales
                final_stats = await monitor.monitor_task(
                    task_id=task_id, total_files=total_files, verbose=verbose
                )

                # Mostrar estadísticas finales
                elapsed = time.time() - start_time

                # Usar estadísticas finales del monitor con casting explícito
                files_processed = int(final_stats.get('files_processed', 0))
                chunks_created = int(final_stats.get('chunks_created', 0))
                embeddings_generated = int(final_stats.get('embeddings_generated', 0))
                files_skipped = int(final_stats.get('files_skipped', 0))
                errors = int(final_stats.get('errors', 0))

                # Calcular métricas
                files_per_second = files_processed / elapsed if elapsed > 0 else 0
                chunks_per_file = chunks_created / files_processed if files_processed > 0 else 0

                # Panel final con resumen
                final_panel = Panel(
                    f"""✅ [bold green]Indexing Completed Successfully![/bold green]
                    
📊 [bold cyan]Final Statistics:[/bold cyan]
• Files Processed: {files_processed}
• Chunks Created: {chunks_created}
• Embeddings Generated: {embeddings_generated}
• Files Skipped: {files_skipped}
• Errors: {errors}
• Total Time: {elapsed:.1f}s
• Average Speed: {files_per_second:.2f} files/second
• Average Chunks per File: {chunks_per_file:.1f}""",
                    style="green",
                    border_style="bright_green",
                    title="🎉 Success",
                )

                layout["progress"].update(final_panel)
                layout["stats"].update(Panel("", style="green"))
                live.update(layout)

                # Pausa para que el usuario vea el resultado
                await asyncio.sleep(2)

            except KeyboardInterrupt:
                # Panel de cancelación
                cancel_panel = Panel(
                    "⚠️ [bold yellow]Progress monitoring cancelled.[/bold yellow]\n"
                    "Indexing continues in background.\n"
                    "Check logs with: [bold]acolyte logs[/bold]",
                    style="yellow",
                    border_style="bright_yellow",
                    title="⏸️ Cancelled",
                )
                layout["progress"].update(cancel_panel)
                live.update(layout)
                await asyncio.sleep(1)

            except Exception as e:
                # Panel de error
                error_panel = Panel(
                    f"❌ [bold red]Error monitoring progress:[/bold red]\n"
                    f"{str(e)}\n\n"
                    f"Check logs with: [bold]acolyte logs[/bold]",
                    style="red",
                    border_style="bright_red",
                    title="💥 Error",
                )
                layout["progress"].update(error_panel)
                live.update(layout)
                await asyncio.sleep(2)

                if os.environ.get('ACOLYTE_DEBUG'):
                    import traceback

                    traceback.print_exc()


async def monitor_indexing_progress_legacy(
    backend_port: int, websocket_path: str, task_id: str, total_files: int, verbose: bool = False
):
    """Legacy monitor - kept for reference."""
    # Lazy imports
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
    from rich.console import Console
    import websockets
    import json

    console = Console()

    # WebSocket URL - using urllib.parse for safe URL construction
    from urllib.parse import urlunparse

    ws_url = urlunparse(('ws', f"localhost:{backend_port}", websocket_path, '', '', ''))

    try:
        # First try WebSocket
        import asyncio

        websocket = await asyncio.wait_for(websockets.connect(ws_url), timeout=5)
        try:
            console.print("[green]✓[/green] Connected to progress monitor")

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TextColumn("•"),
                TextColumn("{task.fields[current_file]}"),
                TimeElapsedColumn(),
                console=console,
            ) as progress:

                main_task = progress.add_task(
                    "[cyan]Indexing files...", total=total_files or 100, current_file="Starting..."
                )

                # Statistics tracking
                stats = {
                    "chunks_created": 0,
                    "embeddings_generated": 0,
                    "files_skipped": 0,
                    "errors": 0,
                }

                async for message in websocket:
                    try:
                        data = json.loads(message)

                        # Handle different message types
                        if data.get('type') == 'progress':
                            # Update progress bar
                            current = data.get('current', 0)
                            total = data.get('total', total_files)
                            current_file = data.get('current_file', data.get('message', ''))

                            # Update statistics if available
                            if 'chunks_created' in data:
                                stats['chunks_created'] = data['chunks_created']
                            if 'embeddings_generated' in data:
                                stats['embeddings_generated'] = data['embeddings_generated']
                            if 'files_skipped' in data:
                                stats['files_skipped'] = data['files_skipped']
                            if 'errors' in data:
                                stats['errors'] = data['errors']

                            progress.update(
                                main_task, completed=current, total=total, current_file=current_file
                            )

                            # Show detailed stats if verbose
                            if verbose and current % 10 == 0:  # Every 10 files
                                console.print(
                                    f"[dim]Chunks: {stats['chunks_created']} | "
                                    f"Embeddings: {stats['embeddings_generated']} | "
                                    f"Skipped: {stats['files_skipped']} | "
                                    f"Errors: {stats['errors']}[/dim]"
                                )

                            # Check if complete
                            if current >= total:
                                progress.update(main_task, completed=total)
                                break

                        elif data.get('type') == 'error':
                            console.print(
                                f"[red]Error: {data.get('message', 'Unknown error')}[/red]"
                            )

                        elif data.get('type') == 'complete':
                            progress.update(main_task, completed=total_files)
                            break

                    except json.JSONDecodeError:
                        # Handle non-JSON messages (like ping/pong)
                        pass
                    except Exception as e:
                        if verbose:
                            console.print(f"[yellow]Warning: {e}[/yellow]")

            # Final statistics
            console.print("\n[bold green]✓ Indexing completed![/bold green]")

            # Show final stats table
            if stats['chunks_created'] > 0 or verbose:
                from rich.table import Table

                table = Table(title="Indexing Statistics")
                table.add_column("Metric", style="cyan")
                table.add_column("Value", style="green")

                table.add_row("Files Processed", str(total_files - stats['files_skipped']))
                table.add_row("Files Skipped", str(stats['files_skipped']))
                table.add_row("Chunks Created", str(stats['chunks_created']))
                table.add_row("Embeddings Generated", str(stats['embeddings_generated']))

                if stats['errors'] > 0:
                    table.add_row("Errors", f"[red]{stats['errors']}[/red]")

                console.print(table)

                if stats['errors'] > 0:
                    console.print(
                        "\n[yellow]⚠ Some files had errors. Check logs for details.[/yellow]"
                    )

        finally:
            await websocket.close()

    except (websockets.ConnectionClosedError, asyncio.TimeoutError):
        # WebSocket failed, fallback to polling
        console.print("[yellow]⚠[/yellow] WebSocket connection failed, using HTTP polling")
        await monitor_via_polling(backend_port, task_id, total_files, console)

    except KeyboardInterrupt:
        console.print(
            "\n[yellow]Progress monitoring cancelled. Indexing continues in background.[/yellow]"
        )

    except Exception as e:
        console.print(f"[red]Error monitoring progress: {e}[/red]")
        if os.environ.get('ACOLYTE_DEBUG'):
            import traceback

            traceback.print_exc()


async def monitor_via_polling(backend_port: int, task_id: str, total_files: int, console):
    """Fallback monitoring via HTTP polling."""
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
    import aiohttp
    import asyncio

    console.print("[dim]Using HTTP polling for progress updates...[/dim]")
    url = f"http://localhost:{backend_port}/api/index/task/{task_id}/status"

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Indexing files...", total=total_files or 100)
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.get(url) as response:
                        if response.status == 200:
                            data = await response.json()
                            current = data.get('processed_files', 0)
                            total = data.get('total_files', total_files)
                            status = data.get('status', 'running')
                            progress.update(task, completed=current, total=total)
                            if status in ['completed', 'failed', 'cancelled']:
                                break
                        else:
                            console.print(
                                f"[yellow]Polling error: status {response.status}[/yellow]"
                            )
                except Exception as e:
                    console.print(f"[yellow]Polling error: {e}[/yellow]")
                await asyncio.sleep(2)
    console.print("\n[bold green]✓ Indexed completed (polling HTTP)[/bold green]")
