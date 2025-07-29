"""
Log formatter for ACOLYTE CLI logs command.
Handles parsing and colorizing various log formats into consistent columns.
"""

import re
from typing import Dict
import click


def colorize_log_line(line: str) -> str:
    """Parse, format and colorize a log line into consistent columns.

    Handles multiple log formats and normalizes them into:
    service | time | level | location | message

    Args:
        line: Raw log line to format

    Returns:
        Colorized and formatted log line
    """
    # Skip empty lines
    if not line.strip():
        return line

    # Define level colors
    level_colors: Dict[str, str] = {
        'TRACE': 'blue',
        'DEBUG': 'blue',
        'INFO': 'white',
        'SUCCESS': 'green',
        'WARNING': 'yellow',
        'WARN': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red',
    }

    # Extract service name if present (e.g., "acolyte-backend   |")
    service_match = re.match(r'^([\w-]+)\s*\|\s*(.*)$', line)
    if service_match:
        service = service_match.group(1)
        rest_of_line = service_match.group(2)
    else:
        # No service prefix, determine service from content
        if (
            line.strip().startswith('INFO:')
            or line.strip().startswith('WARNING:')
            or line.strip().startswith('ERROR:')
        ):
            service = 'uvicorn'
        elif line.strip().startswith('[GIN]'):
            service = 'acolyte-ollama'  # GIN logs come from ollama container
        elif (
            line.strip().startswith('llama_')
            or line.strip().startswith('print_info:')
            or line.strip().startswith('load')
        ):
            service = 'acolyte-ollama'
        elif 'time=' in line and 'level=' in line:
            service = 'acolyte-ollama'
        else:
            service = 'system'
        rest_of_line = line.strip()

    # Initialize default values
    time_str = '00:00:00'
    level = 'INFO'
    location = 'unknown'
    message = rest_of_line

    # Try to parse different formats

    # Format 1: Standard loguru format with 4 parts
    # HH:mm:ss | LEVEL     | module:function | message
    parts = rest_of_line.split(' | ')
    if len(parts) == 4:
        time_str = parts[0].strip()
        level = parts[1].strip()
        location = parts[2].strip()
        message = parts[3].strip()

    # Format 2: Old format with 3 parts
    # YYYY-MM-DD HH:mm:ss.SSS | LEVEL | message
    elif len(parts) == 3:
        time_part = parts[0].strip()
        # Extract just time from datetime
        if ' ' in time_part:
            time_str = time_part.split(' ')[1]
        else:
            time_str = time_part
        level = parts[1].strip()
        location = 'acolyte'
        message = parts[2].strip()

    # Format 3: Uvicorn logs without timestamp
    # INFO:     Started server process [1]
    elif (
        rest_of_line.startswith('INFO:')
        or rest_of_line.startswith('WARNING:')
        or rest_of_line.startswith('ERROR:')
    ):
        level_match = re.match(r'^(\w+):\s*(.*)$', rest_of_line)
        if level_match:
            level = level_match.group(1)
            message = level_match.group(2)

            # Try to extract more specific location from message
            if 'server process' in message:
                location = 'uvicorn.server:startup'
            elif 'Application startup' in message:
                location = 'uvicorn.app:startup'
            elif 'Uvicorn running on' in message:
                location = 'uvicorn.server:main'
            elif ' - ' in message and 'HTTP' in message:
                # HTTP request log: "172.18.0.1:37272 - "GET /api/health HTTP/1.1" 200 OK"
                location = 'uvicorn.access:http'
            else:
                location = 'uvicorn.server:info'

    # Format 4: Ollama logs with time=... level=... format
    # time=2025-07-08T20:54:27.860Z level=INFO source=server.go:637 msg="..."
    elif 'time=' in rest_of_line and 'level=' in rest_of_line:
        time_match = re.search(r'time=([\w\-:.]+)', rest_of_line)
        level_match = re.search(r'level=(\w+)', rest_of_line)
        source_match = re.search(r'source=([\w.:]+)', rest_of_line)
        msg_match = re.search(r'msg="([^"]+)"', rest_of_line)

        if time_match:
            # Extract just time from ISO timestamp
            iso_time = time_match.group(1)
            if 'T' in iso_time:
                time_str = iso_time.split('T')[1].split('Z')[0][:8]

        if level_match:
            level = level_match.group(1)

        if source_match:
            location = 'ollama.' + source_match.group(1)
        else:
            location = 'ollama.server'

        if msg_match:
            message = msg_match.group(1)
        else:
            message = rest_of_line

    # Format 5: GIN logs - NORMALIZE TO STANDARD FORMAT
    # [GIN] 2025/07/08 - 20:54:29 | 200 |          1m2s |       127.0.0.1 | POST     "/api/generate"
    elif rest_of_line.startswith('[GIN]'):
        gin_match = re.match(
            r'\[GIN\]\s+(\d{4}/\d{2}/\d{2})\s+-\s+(\d{2}:\d{2}:\d{2})\s+\|\s+(\d+)\s+\|\s+([^|]+)\|\s+([^|]+)\|\s+(\w+)\s+"([^"]+)"',
            rest_of_line,
        )
        if gin_match:
            time_str = gin_match.group(2)
            status_code = gin_match.group(3)
            duration = gin_match.group(4).strip()
            ip = gin_match.group(5).strip()
            method = gin_match.group(6)
            path = gin_match.group(7)

            # Set level based on status code
            if status_code.startswith('2'):
                level = 'INFO'
            elif status_code.startswith('4'):
                level = 'WARNING'
            elif status_code.startswith('5'):
                level = 'ERROR'
            else:
                level = 'INFO'

            # Format location like other logs
            location = f'gin.http:{method.lower()}'
            # Format message consistently
            message = f'[{status_code}] {path} ({duration}) from {ip}'
        else:
            # Fallback for malformed GIN logs
            time_str = '00:00:00'
            level = 'INFO'
            location = 'gin.http:unknown'
            message = rest_of_line[5:]  # Remove [GIN]

    # Format 6: llama_model_loader, print_info, llama_context, etc.
    elif (
        rest_of_line.startswith('llama_')
        or rest_of_line.startswith('print_info:')
        or rest_of_line.startswith('load:')
        or rest_of_line.startswith('load_tensors:')
    ):
        prefix_match = re.match(r'^([\w_]+):\s*(.*)$', rest_of_line)
        if prefix_match:
            prefix = prefix_match.group(1)
            message = prefix_match.group(2)

            # Group similar prefixes
            if prefix.startswith('llama_'):
                location = f'ollama.{prefix}'
            elif prefix == 'print_info':
                location = 'ollama.loader:info'
            elif prefix in ['load', 'load_tensors']:
                location = f'ollama.loader:{prefix}'
            else:
                location = f'ollama.{prefix}'
        else:
            location = 'ollama.system'
            message = rest_of_line

    # Format 7: Simple line (like "Aborted!")
    else:
        # Check if it's just a simple message
        if ' | ' not in rest_of_line and ':' not in rest_of_line:
            level = 'INFO'
            location = 'system:message'
            message = rest_of_line

    # Format columns with fixed widths for alignment
    service_col = service.ljust(17)  # 17 chars for service name
    time_col = time_str[:8].ljust(8)  # 8 chars for time
    level_col = level.ljust(8)  # 8 chars for level
    location_col = location[:40].ljust(40)  # 40 chars for location

    # Get level color
    level_color = level_colors.get(level.upper(), 'white')

    # Build colored line
    colored_line = (
        click.style(service_col, fg='magenta')
        + ' | '
        + click.style(time_col, fg='green')
        + ' | '
        + click.style(level_col, fg=level_color)
        + ' | '
        + click.style(location_col, fg='cyan')
        + ' | '
        + click.style(message, fg=level_color)
    )

    return colored_line
