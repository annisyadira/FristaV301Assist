# BPJS Frista Automation

A Windows automation project for interacting with the Frista BPJS Kesehatan desktop application v3.0.1. It can launch the Frista application, log in using local configuration, submit a BPJS or KTP number, and expose a small local HTTP bridge for starting the packaged application.

## Features

- Automates the Frista desktop application with `pywinauto`.
- Logs in using credentials stored in a local configuration file.
- Passes a BPJS or KTP number to the Frista application.
- Provides a Flask endpoint for launching `app.exe`.
- Includes a small UI inspection tool for Windows application controls.

## Requirements

- Windows
- Python 3.10 or newer
- Access to the Frista BPJS Kesehatan desktop application v3.0.1
- Permission to use the application and its credentials

Install the Python dependencies:

```powershell
python -m pip install flask pywinauto PyQt5 pyinstaller
```

## Configuration

Create a local `config.txt` file in the project root. This file is ignored by Git because it may contain credentials:

```text
# where to send the data. can be .txt file or an .exe file
destination==C:\\Path\\To\\frista.exe

# credentials
username==your_username
password==your_password
```

The current implementation expects the password value in Base64 format. Base64 is not encryption, so do not treat it as a security mechanism. Keep this file private and use a dedicated, least-privileged account.

The Frista executable must already be installed and accessible at the configured `destination` path.

## Usage

### Run the automation directly

Pass a BPJS or KTP number to the automation script:

```powershell
python app.py --fristainput 1234567890
```

When the destination ends in `.exe`, the script connects to or starts the Frista application, logs in when needed, and enters the supplied number.

### Run the local API bridge

Start the Flask bridge:

```powershell
python api.py
```

The bridge exposes `POST /app`. Example request:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:5000/app `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"key":"your-local-key","args":["--fristainput","1234567890"]}'
```

The API implementation currently uses a hardcoded key and is intended for local development only. Do not expose it to the public internet without authentication, strict input validation, and a safer process-launching design.

### Inspect Windows controls

Run the inspection utility to view controls exposed by a Windows application:

```powershell
python py_inspect.py
```

## Security and privacy

This project interacts with a BPJS Kesehatan application and may process sensitive identifiers such as BPJS or KTP numbers. Before sharing the project publicly:

- Never commit `config.txt`, credentials, API keys, or personal data.
- Rotate any credential that has already been exposed.
- Keep `build/`, `dist/`, executables, and ZIP archives out of the repository unless they have been reviewed.
- Do not run the Flask bridge with `debug=True` outside local development.
- Keep the bridge bound to localhost unless a secured deployment is explicitly required.
- Validate and restrict all command arguments before launching a process.
- Follow your organization's policies and BPJS Kesehatan's terms when handling data and automation.

## Project files

|        File        |                          Description                            |
| ------------------ | --------------------------------------------------------------- |
| `app.py`           | Main Frista desktop automation script.                          |
| `api.py`           | Local Flask bridge for launching the packaged application.      |
| `find_elements.py` | Example script for locating Frista window controls.             |
| `py_inspect.py`    | Windows UI inspection utility.                                  |
| `config.conf`      | Application/API configuration reference.                        |
| `config.txt`       | Local credentials and destination configuration; do not commit. |
| `*.spec`           | PyInstaller build specifications.                               |

## Disclaimer

This project is provided for authorized internal automation and testing only. The user is responsible for access rights, data protection, and compliance with applicable policies and regulations.
