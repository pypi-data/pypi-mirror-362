"""
ACOLYTE Chat Command - Interactive chat with your indexed project
"""

import sys
from pathlib import Path

import yaml
import requests
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt


def run_chat(path: str, debug: bool, explain_rag: bool, project_manager):
    """Execute the chat command with the indexed project"""
    console = Console()
    project_path = Path(path)

    # Check if project is initialized
    if not project_manager.is_project_initialized(project_path):
        console.print("[bold red]✗ Project not initialized![/bold red]")
        console.print("Run 'acolyte init' first")
        sys.exit(1)

    # Load project info and config
    project_info = project_manager.load_project_info(project_path)
    if not project_info:
        console.print("[bold red]✗ Failed to load project info![/bold red]")
        sys.exit(1)

    project_id = project_info['project_id']
    project_dir = project_manager.get_project_dir(project_id)
    config_file = project_dir / ".acolyte"

    if not config_file.exists():
        console.print("[bold red]✗ Project not configured![/bold red]")
        console.print("Run 'acolyte install' first")
        sys.exit(1)

    # Load configuration
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        console.print(f"[bold red]✗ Failed to load configuration: {e}[/bold red]")
        sys.exit(1)

    # Get backend port
    backend_port = config.get('ports', {}).get('backend', 8000)
    backend_url = f"http://localhost:{backend_port}"

    # Check if backend is running
    try:
        health_response = requests.get(f"{backend_url}/api/health", timeout=5)
        if health_response.status_code != 200:
            console.print("[bold red]✗ Backend is not healthy![/bold red]")
            console.print("Run 'acolyte start' first")
            sys.exit(1)
    except requests.RequestException:
        console.print("[bold red]✗ Backend is not running![/bold red]")
        console.print("Run 'acolyte start' first")
        sys.exit(1)

    # Welcome message
    console.print(
        Panel.fit(
            "[bold cyan]🤖 ACOLYTE Chat[/bold cyan]\n\n"
            f"[dim]Project: {project_info.get('name', 'Unknown')}[/dim]\n"
            f"[dim]Indexed files ready for questions[/dim]\n\n"
            "[dim]Type 'exit' or 'quit' to end chat[/dim]"
        )
    )

    # Chat loop
    messages = []

    while True:
        try:
            # Get user input
            user_input = Prompt.ask("\n[bold green]You[/bold green]", default="")

            if user_input.lower() in ['exit', 'quit', 'bye']:
                console.print("\n[dim]Goodbye! 👋[/dim]")
                break

            if not user_input.strip():
                continue

            # Add user message
            messages.append({"role": "user", "content": user_input})

            # Prepare request
            request_data = {
                "model": config['model']['name'],
                "messages": messages,
                "temperature": 0.7,
                "debug": debug,
                "explain_rag": explain_rag,
            }

            # Show loading
            with console.status("[bold blue]🤔 Thinking..."):
                try:
                    response = requests.post(
                        f"{backend_url}/v1/chat/completions",
                        json=request_data,
                        headers={"Content-Type": "application/json"},
                        timeout=30,
                    )

                    if response.status_code != 200:
                        console.print(f"[bold red]✗ Error: {response.status_code}[/bold red]")
                        console.print(f"[red]{response.text}[/red]")
                        continue

                    result = response.json()

                except requests.RequestException as e:
                    console.print(f"[bold red]✗ Request failed: {e}[/bold red]")
                    continue

            # Extract response
            if "choices" in result and len(result["choices"]) > 0:
                assistant_message = result["choices"][0]["message"]["content"]
                messages.append({"role": "assistant", "content": assistant_message})

                # Display response
                console.print("\n[bold blue]🤖 ACOLYTE[/bold blue]")
                console.print(Markdown(assistant_message))

                # Show debug info if requested
                if debug and "debug_info" in result:
                    debug_info = result["debug_info"]
                    console.print("\n[dim]--- Debug Info ---[/dim]")
                    console.print(
                        f"[dim]Chunks found: {debug_info.get('chunks_found', 'N/A')}[/dim]"
                    )
                    console.print(
                        f"[dim]Processing time: {debug_info.get('processing_time_ms', 'N/A')}ms[/dim]"
                    )
                    console.print(
                        f"[dim]Tokens used: {result.get('usage', {}).get('total_tokens', 'N/A')}[/dim]"
                    )

                # Show RAG explanation if requested
                if explain_rag and "rag_explanation" in result:
                    rag_info = result["rag_explanation"]
                    console.print("\n[dim]--- RAG Explanation ---[/dim]")
                    console.print(f"[dim]Strategy: {rag_info.get('search_strategy', 'N/A')}[/dim]")
                    console.print(
                        f"[dim]Chunks retrieved: {rag_info.get('chunks_retrieved', 'N/A')}[/dim]"
                    )

            else:
                console.print("[bold red]✗ No response received[/bold red]")

        except KeyboardInterrupt:
            console.print("\n[dim]Chat interrupted. Goodbye! 👋[/dim]")
            break
        except Exception as e:
            console.print(f"[bold red]✗ Unexpected error: {e}[/bold red]")
            continue
