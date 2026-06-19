# LogMask Engine

A lightweight Python utility that parses structured log entries, anonymizes IP addresses, and surfaces error events.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](#requirements)

## Description

LogMask Engine reads plain-text log entries in the format `<date> <ip> <level> <message>` and extracts them into structured records using a single regular expression. Every IP address found in the log is automatically masked on its last octet (e.g. `192.168.1.15` → `192.168.1.x`), making it safer to share logs externally without exposing exact client addresses. The script also generates a quick console report listing only `ERROR`-level events. It is intended for engineers and SREs who need a minimal, dependency-free starting point for log redaction and triage.

## Table of Contents

- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage / Quick Start](#usage--quick-start)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Key Features

- **Pattern-based log parsing** — extracts `date`, `ip`, `level`, and `message` fields from raw text using a single named-group regular expression.
- **Automatic IP anonymization** — replaces the last octet of every parsed IP address with `x`, so logs can be shared without exposing full client addresses.
- **Structured output** — `parse_logs()` returns a plain list of dictionaries, ready to feed into other scripts, exporters, or reports.
- **Built-in error reporting** — running the script prints a filtered, human-readable report of all `ERROR`-level entries.
- **Zero external dependencies** — uses only the Python standard library (`re`), so there is nothing to install beyond Python itself.

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3 |
| Core library | `re` (standard library) |
| Dependencies | None (standard library only) |

## Requirements

- Python **3.6 or later** (the code uses f-strings, introduced in 3.6)
- No third-party packages required
- No specific OS requirement — runs anywhere Python 3 runs (Linux, macOS, Windows)

## Installation

Clone the repository:

```bash
git clone https://github.com/eryks23/LogMask-Engine.git
cd LogMask-Engine
```

(Optional) Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies (currently none, kept for future use):

```bash
pip install -r requirements.txt
```

No build step is required — the script runs directly with the Python interpreter.

## Configuration

LogMask Engine does not currently use environment variables or external configuration files. All inputs are defined directly in `log_parser.py`:

- `log_data` — a hardcoded sample log string used when the script is run directly.
- The parsing regular expression inside `parse_logs()` — defines the expected log format and accepted severity levels (`INFO`, `WARNING`, `ERROR`).

To process your own logs, replace the `log_data` value or call `parse_logs()` with your own string (see [Usage / Quick Start](#usage--quick-start)).

## Usage / Quick Start

### Run the bundled demo

Running the script directly parses the sample log data included in the file and prints a report of all `ERROR` entries:

```bash
python log_parser.py
```

Expected output:

```
--- ERROR Report ---
[2026-03-06] | IP: 10.0.0.x | Error: Database connection failed
[2026-03-06] | IP: 192.168.1.x | Error: Unauthorized access attempt
```

### Use `parse_logs()` with your own data

```python
from log_parser import parse_logs

custom_logs = """
2026-04-01 10.10.10.42 ERROR Disk write failure
2026-04-01 192.168.0.10 INFO Backup completed
"""

entries = parse_logs(custom_logs)
for entry in entries:
    print(entry)
```

> **Note:** `log_parser.py` does not currently guard its demo code behind an `if __name__ == "__main__":` block. Importing the module will also execute the bundled demo and print the sample `ERROR` report to the console. Keep this in mind if you import `parse_logs` into another script (see [Roadmap](#roadmap)).

## API Documentation

### `parse_logs(data: str) -> list[dict[str, str]]`

Parses raw log text and returns a list of structured, IP-masked log entries.

**Parameters**

| Name | Type | Description |
|---|---|---|
| `data` | `str` | Raw, multi-line log text. Each line is expected to follow the format `YYYY-MM-DD <IP> <LEVEL> <message>`. |

**Returns**

`list[dict[str, str]]` — one dictionary per matched line, with the following keys:

| Key | Type | Description |
|---|---|---|
| `date` | `str` | Log date in `YYYY-MM-DD` format. |
| `ip` | `str` | IP address with the last octet replaced by `x` (e.g. `192.168.1.x`). |
| `level` | `str` | Severity level: `INFO`, `WARNING`, or `ERROR`. |
| `message` | `str` | Remaining free-text message on the line. |

**Behavior notes**

- Lines that do not match the expected format are silently skipped — no error is raised.
- Matching is performed with `re.finditer`, so the function correctly handles multi-line input.
- Only the levels `INFO`, `WARNING`, and `ERROR` are recognized; any other level value will cause the line to be skipped.

**Example**

```python
>>> from log_parser import parse_logs
>>> parse_logs("2026-03-06 192.168.1.15 INFO User logged in")
[{'date': '2026-03-06', 'ip': '192.168.1.x', 'level': 'INFO', 'message': 'User logged in'}]
```

## Project Structure

```
LogMask-Engine/
├── log_parser.py     # Core script: log parsing, IP masking, ERROR report generation
├── requirements.txt  # Python dependencies (none currently required)
├── LICENSE           # MIT License
└── README.md         # Project documentation
```

## Testing

This repository does not yet include an automated test suite. To verify behavior manually:

```bash
python log_parser.py
```

Confirm the output matches the report shown in [Usage / Quick Start](#usage--quick-start). Adding automated tests (e.g. with `pytest` or the standard `unittest` module) against `parse_logs()` is tracked in the [Roadmap](#roadmap).

## Roadmap

The following improvements are not yet implemented but follow directly from the current state of the code:

- [ ] Guard the demo execution with `if __name__ == "__main__":` to make the module safely importable.
- [ ] Add an automated test suite (`pytest` or `unittest`) covering `parse_logs()`.
- [ ] Accept a log file path or CLI arguments (e.g. via `argparse`) instead of relying on a hardcoded sample string.
- [ ] Support additional severity levels and configurable log formats.
- [ ] Add export options for parsed results (JSON, CSV).

## Contributing

Contributions are welcome. To propose a change:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`.
3. Make your changes and add tests where applicable.
4. Commit with a clear message: `git commit -m "Add: your change description"`.
5. Push your branch and open a pull request against `main`.

Please keep changes focused and explain the motivation for the change in the pull request description.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Contact

- **Repository:** [github.com/eryks23/LogMask-Engine](https://github.com/eryks23/LogMask-Engine)
- **Author:** [eryks23](https://github.com/eryks23)
