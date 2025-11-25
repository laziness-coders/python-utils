"""Example showing how to emit logs using python-utils.

Run this script after installing the package locally:

    pip install .
    LOG_API_URL="https://logging.example.com/logs" LOG_API_KEY="your-api-key" python examples/basic_logging.py
"""
from python_utils import send_info, send_warning, send_error, send_critical


def main() -> None:
    send_info("Starting price update pipeline")
    send_warning("Fallback to cached catalog because live source was slow")
    send_error("Failed to update price for SKU-12345")
    send_critical("Terminating pipeline after repeated failures")


if __name__ == "__main__":
    main()
