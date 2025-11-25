"""
Centralized logging module for GSC WooCommerce price update system.
Provides a unified send_log function for sending logs to the remote logging API.
"""

from __future__ import annotations

import hashlib
import inspect
import json
import os
from datetime import datetime

import requests


def send_log(level: str, message: str) -> bool:
    """
    Send log message to remote logging API.

    Args:
        level (str): Log level (e.g., 'info', 'warning', 'error', 'critical')
        message (str): Log message to send

    Returns:
        bool: True if log was sent successfully, False otherwise
    """
    log_api_url = os.environ.get("LOG_API_URL")
    log_api_key = os.environ.get("LOG_API_KEY")

    if not log_api_url or not log_api_key:
        print("Error: LOG_API_URL and LOG_API_KEY environment variables must be set")
        return False

    frame = inspect.currentframe().f_back
    while frame and frame.f_code.co_filename.endswith("logger.py"):
        frame = frame.f_back

    if frame:
        filepath = frame.f_code.co_filename
        line_number = frame.f_lineno
    else:
        filepath = "unknown"
        line_number = 0

    dedup_key = hashlib.md5(f"{filepath}:{line_number}".encode("utf-8")).hexdigest()
    formatted_message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{filepath}:{line_number}] {message}"

    payload = {
        "level": level,
        "message": formatted_message,
        "dedup_key": dedup_key,
    }

    headers = {
        "Authorization": f"Bearer {log_api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            log_api_url,
            headers=headers,
            data=json.dumps(payload),
            timeout=5,
        )
        response.raise_for_status()
        print("Log sent successfully:", response.text)
        return True
    except requests.exceptions.RequestException as err:  # pragma: no cover - network errors
        print("Error sending log:", err)
        return False


def send_info(message: str) -> bool:
    """Send info level log message."""

    return send_log("info", message)


def send_warning(message: str) -> bool:
    """Send warning level log message."""

    return send_log("warning", message)


def send_error(message: str) -> bool:
    """Send error level log message."""

    return send_log("error", message)


def send_critical(message: str) -> bool:
    """Send critical level log message."""

    return send_log("critical", message)
