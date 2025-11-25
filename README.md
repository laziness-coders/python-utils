# python-utils

Utility helpers for Python projects. The initial release provides a centralized logging helper that sends JSON log payloads to a remote API using an API key.

## Installation

```bash
pip install .
```

To install the package directly into another project via pip, point to the repository URL:

```bash
pip install "git+https://github.com/laziness-coders/python-utils.git@main"
```

In a `requirements.txt` file you can pin a version or branch:

```
python-utils @ git+https://github.com/laziness-coders/python-utils.git@v1.0.0
```

### Why `pyproject.toml`?
- Defines build requirements and metadata in a single, modern standard that pip understands, so `pip install .` works reliably.
- Lets packaging tools discover the source layout (`src/` in this repo) without additional configuration files.
- Ensures dependency declaration (`requests`) is installed automatically when the package is consumed.

## Logging helper

The `python_utils.logger` module exposes convenience functions for sending logs to a remote API endpoint. Configure the endpoint with environment variables before calling `send_log` or its level-specific wrappers.

```bash
export LOG_API_URL="https://logging.example.com/logs"
export LOG_API_KEY="your-api-key"
```

```python
from python_utils import send_info, send_error

send_info("Background job started")
send_error("Could not fetch product catalog")
```

### Behavior
- Includes caller file path and line number in the message for easier tracing.
- Generates an MD5-based `dedup_key` derived from the caller location to reduce duplicate log entries.
- Uses a short timeout (5 seconds) when contacting the remote API and returns `False` on failure.

### API
- `send_log(level: str, message: str) -> bool`
- `send_info(message: str) -> bool`
- `send_warning(message: str) -> bool`
- `send_error(message: str) -> bool`
- `send_critical(message: str) -> bool`

## Examples

Run the included example script after setting your logging endpoint environment variables:

```bash
pip install .
LOG_API_URL="https://logging.example.com/logs" LOG_API_KEY="your-api-key" python examples/basic_logging.py
```
