# Log Viewer

Provides a way to securely watch a server-side log file in real-time.

# Installation

## Prerequisites

- Python 3+ (+venv)
- Make

## Setup python virtual environment

```
make venv
```

## Activate python virtual environment

```
source venv/bin/activate
```

# Configuration

## Environment Variables

| Variable     | Default          | Description                                                                      |
| ------------ | ---------------- | -------------------------------------------------------------------------------- |
| FILE_PATH    | None             | File to watch. Required.                                                         |
| LOCALE       | en_US            | Controls what locale is used across the app.                                     |
| TIMEZONE     | US/Eastern       | Controls what timezone to use when a date+time is displayed.                     |
| AUTH_ENABLED | 1                | Controls if authentication is required.                                          |
| AUTH_FILE    | .log-viewer-auth | File to use for authentication. File should be in username:password line format. |
| INDEX_TITLE  | Home             | Displayed in the main page header.                                               |

# Launch in debug mode (non-wsgi)

This **should not** be used in production.

```
flask --app path/to/log-viewer run \
 -h localhost \
 -p 3000 \
 --debug
```

# Launch in production mode

### Gunicorn

```
pip install gunicorn eventlet
gunicorn -b localhost:3000 --worker-class eventlet -w 1 --chdir /path/to log-viewer:app
```

Flask SocketIO does not appear to support multiple workers in gunicorn.