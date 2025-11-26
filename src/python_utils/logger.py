"""
Centralized logging utility to send log messages to a remote logging API.
Provides functions for different log levels: info, warning, error, and critical.
"""

from __future__ import annotations

import hashlib
import inspect
import json
import os
import traceback
from datetime import datetime

import requests


def send_log(
    level: str,
    message: str | Exception,
) -> bool:
    """
    Send log message to remote logging API.

    Args:
        level (str): Log level (e.g., 'info', 'warning', 'error', 'critical')
        message (str | Exception): Log message to send or exception to format and log

    Returns:
        bool: True if log was sent successfully, False otherwise
    """
    log_api_url = os.environ.get("LOG_API_URL")
    log_api_key = os.environ.get("LOG_API_KEY")

    if not log_api_url or not log_api_key:
        print("Error: LOG_API_URL and LOG_API_KEY environment variables must be set")
        return False

    if isinstance(message, Exception):
        formatted_message = format_exception_message(message)
    else:
        formatted_message = format_string_message(message)

    dedup_key = hashlib.md5(f"{formatted_message}".encode("utf-8")).hexdigest()
    formatted_message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {formatted_message}"

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


def send_info(message: str | Exception) -> bool:
    """Send info level log message."""

    return send_log("info", message)


def send_warning(message: str | Exception) -> bool:
    """Send warning level log message."""

    return send_log("warning", message)


def send_error(message: str | Exception) -> bool:
    """Send error level log message."""

    return send_log("error", message)


def send_critical(message: str | Exception) -> bool:
    """Send critical level log message."""

    return send_log("critical", message)


def format_exception_message(e: Exception) -> str:
    """
    Format exception message as: file_path:line_number exception_message (EXCEPTION:ExceptionType)

    Args:
        e: Exception object

    Returns:
        Formatted exception string
    """
    tb = traceback.extract_tb(e.__traceback__)
    exception_type = type(e).__name__
    exception_message = str(e)

    if tb:
        last_frame = tb[-1]
        file_path = last_frame.filename
        line_number = last_frame.lineno
        return f"{file_path}:{line_number} {exception_message} (EXCEPTION:{exception_type})"
    else:
        return f"{exception_message} (EXCEPTION:{exception_type})"


def format_string_message(message: str) -> str:
    """
    Format a string message with filepath and line number by inspecting the call stack.

    Args:
        message: The log message string

    Returns:
        Formatted message string
    """
    frame = inspect.currentframe().f_back
    while frame and frame.f_code.co_filename.endswith("logger.py"):
        frame = frame.f_back

    if frame:
        filepath = frame.f_code.co_filename
        line_number = frame.f_lineno
    else:
        filepath = "unknown"
        line_number = 0

    formatted_message = f"[{filepath}:{line_number}] {message}"
    return formatted_message
