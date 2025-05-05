# Echo Bot

A simple echo bot for the HumanOrBot project that replies to any received message with the same text.

## Overview

This service provides a FastAPI-based API endpoint that receives messages and echoes them back. It is designed to work with the HumanOrBot service, responding to each message with the same text.

## Running the Service

### On Linux/macOS

```bash
chmod +x run_all_linux.sh
./run_all_linux.sh
```

### On Windows

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\run_all_windows.ps1
```

#### These scripts will:
1. Install Poetry (if needed)
2. Install project dependencies
3. Set up an SSH tunnel to the remote host
4. Start the FastAPI application on port 6782

## Development

To run tests:

```bash
poetry run python -m unittest discover -v tests
```