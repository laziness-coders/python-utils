# python-utils

Utility helpers for Python projects. The initial release provides a centralized logging helper that sends JSON log payloads to a remote API using an API key.

## Installation

### Using a Virtual Environment (Recommended)

On macOS and modern Linux systems, Python environments are externally managed. Always use a virtual environment:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install the package
pip install "git+https://github.com/laziness-coders/python-utils.git@main"
```

**Note:** If you're not using a virtual environment and your system has both Python 2 and Python 3, use `pip3` instead of `pip`:

```bash
pip3 install "git+https://github.com/laziness-coders/python-utils.git@main"
```

### Local Development Installation

If you've cloned the repository locally:

```bash
# Activate your virtual environment first
source venv/bin/activate

# Install in editable mode (changes reflect immediately)
pip install -e .

# Or install normally
pip install .
```

### In requirements.txt

Add to your project's `requirements.txt`:

```
python-utils @ git+https://github.com/laziness-coders/python-utils.git@main
```

Or pin to a specific version/tag:

```
python-utils @ git+https://github.com/laziness-coders/python-utils.git@v0.1.0
```

Then install with:

```bash
pip install -r requirements.txt
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
# Make sure you're in a virtual environment
source venv/bin/activate

# Install the package
pip install .

# Run the example
LOG_API_URL="https://logging.example.com/logs" LOG_API_KEY="your-api-key" python examples/basic_logging.py
```
