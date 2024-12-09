# Log Viewer

Provides a way to securely watch a server-side log file in real-time.

## Licensing

This project is released under the MIT License.

See `LICENSE.md` for your copy.

## Usage Disclaimer

THERE IS NO WARRANTY FOR THE SOFTWARE, TO THE EXTENT PERMITTED BY APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE SOFTWARE “AS IS” WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SOFTWARE IS WITH THE CUSTOMER. SHOULD THE SOFTWARE PROVE DEFECTIVE, THE CUSTOMER ASSUMES THE COST OF ALL NECESSARY SERVICING, REPAIR, OR CORRECTION EXCEPT TO THE EXTENT SET OUT UNDER THE HARDWARE WARRANTY IN THESE TERMS. BY USING THIS SOFTWARE, YOU AGREE WITH THESE TERMS.

## Installation

### Prerequisites

- Python 3+ (+venv)
- Make

### Setup python virtual environment

```
make venv
```

### Activate python virtual environment

```
source venv/bin/activate
```

## Configuration

### Environment Variables

| Variable     | Default          | Description                                                                      |
| ------------ | ---------------- | -------------------------------------------------------------------------------- |
| FILE_PATH    | None             | File to watch. Required.                                                         |
| LOCALE       | en_US            | Controls what locale is used across the app.                                     |
| TIMEZONE     | US/Eastern       | Controls what timezone to use when a date+time is displayed.                     |
| AUTH_ENABLED | 1                | Controls if authentication is required.                                          |
| AUTH_FILE    | .log-viewer-auth | File to use for authentication. File should be in username:password line format. |
| INDEX_TITLE  | Home             | Displayed in the main page header.                                               |

## Launch in debug mode (non-wsgi)

This **should not** be used in production.

```
flask --app path/to/log-viewer run \
 -h localhost \
 -p 3000 \
 --debug
```

See the `run_debug.sh-example`  file for a template shell script to use.

## Launch in production mode

### Gunicorn

```
pip install gunicorn eventlet
gunicorn -b localhost:3000 --worker-class eventlet -w 1 --chdir /path/to log-viewer:app
```

Flask SocketIO does not appear to support multiple workers in gunicorn.

See the `run_production.sh-example`  file for a template shell script to use.