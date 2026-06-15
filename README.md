# Water Hyacinth Collection Boat Control System - Phase 8

Phase 1 implemented authentication. Phase 2 adds live camera streaming only.
Phase 3 adds backend Arduino serial command testing only.
Phase 4 adds dashboard control buttons that send serial commands.
Phase 8 adds Raspberry Pi deployment files for Gunicorn and systemd.

## Features

- User registration
- Password hashing
- User login
- User logout
- Protected dashboard route
- SQLite database with Flask-SQLAlchemy
- Bootstrap-based pages
- OpenCV camera support
- MJPEG live video stream at `/video_feed`
- Camera connection status on the dashboard
- Graceful offline frame when the camera is unavailable
- PySerial support
- Arduino serial port auto-detection
- 9600 baud Arduino connection
- Validated backend test commands: `F`, `B`, `L`, `R`, `S`
- Test command endpoint at `POST /api/test-command`
- Graceful Arduino disconnect handling
- Mobile-friendly boat control panel
- Press-and-hold movement controls
- Stop command sent automatically on button release
- Control endpoint at `POST /api/control`
- Gunicorn deployment entry point
- systemd service for automatic startup on Raspberry Pi boot

## Project Structure

```text
Boat_Project/
|-- app/
|   |-- __init__.py
|   |-- camera.py
|   |-- models.py
|   |-- serial_controller.py
|   |-- auth/
|   |   |-- __init__.py
|   |   `-- routes.py
|   |-- main/
|   |   |-- __init__.py
|   |   `-- routes.py
|   `-- templates/
|       |-- base.html
|       |-- dashboard.html
|       |-- login.html
|       `-- register.html
|-- config.py
|-- deployment/
|   |-- boat-control.service
|   |-- gunicorn.conf.py
|   `-- INSTALL_RASPBERRY_PI.md
|-- README.md
|-- requirements.txt
|-- wsgi.py
`-- run.py
```

The SQLite database is created automatically at:

```text
instance/boat_control.db
```

## Setup Instructions

1. Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the application:

```powershell
python run.py
```

4. Open the app:

```text
http://127.0.0.1:5000
```

## Raspberry Pi Deployment

Deployment files are in `deployment/`.

Follow:

```text
deployment/INSTALL_RASPBERRY_PI.md
```

The systemd service file is:

```text
deployment/boat-control.service
```

The Gunicorn config file is:

```text
deployment/gunicorn.conf.py
```

## Testing Instructions

1. Start the app with `python run.py`.
2. Go to `http://127.0.0.1:5000/register`.
3. Register a new user with a username and password.
4. Log in at `http://127.0.0.1:5000/login`.
5. Confirm you are redirected to the protected dashboard.
6. Confirm the Live Camera Feed section appears.
7. Confirm the camera status badge shows whether the camera is connected.
8. Confirm `http://127.0.0.1:5000/video_feed` returns an MJPEG stream while logged in.
9. Disconnect or block the camera and refresh the dashboard.
10. Confirm the dashboard shows a disconnected status and the stream displays an offline frame instead of crashing.
11. Connect an Arduino by USB and make sure its sketch accepts single-character serial commands at 9600 baud.
12. While logged in, send a test command:

```powershell
curl -X POST http://127.0.0.1:5000/api/test-command `
  -H "Content-Type: application/json" `
  -b "session=<your-session-cookie>" `
  -d "{\"command\":\"F\"}"
```

13. Confirm a valid command returns a JSON response with `"success": true`.
14. Send an invalid command such as `"X"` and confirm the endpoint returns a validation error.
15. Disconnect the Arduino and send another valid command.
16. Confirm the endpoint returns a graceful disconnect or detection message instead of crashing.
17. On the dashboard, confirm the control panel appears beside or below the camera feed depending on screen size.
18. Press and hold Forward.
19. Confirm the frontend sends `F` to `POST /api/control`.
20. Release Forward.
21. Confirm the frontend sends `S` to `POST /api/control`.
22. Repeat for Left, Right, Backward, and Stop.
23. Disconnect the Arduino and press a control button.
24. Confirm the dashboard shows a graceful warning instead of crashing.
25. Visit `http://127.0.0.1:5000/logout`.
26. Try opening `http://127.0.0.1:5000/dashboard` while logged out.
27. Confirm Flask-Login redirects you back to the login page.

For quick API testing without manually copying a browser session cookie, use Flask's test client:

```powershell
.\venv\Scripts\python.exe -c "from app import create_app; app=create_app(); c=app.test_client(); print(c.post('/api/test-command', json={'command':'F'}).status_code)"
```

The unauthenticated test should return `302`, proving the endpoint is protected.

You can also check the control endpoint protection:

```powershell
.\venv\Scripts\python.exe -c "from app import create_app; app=create_app(); c=app.test_client(); print(c.post('/api/control', json={'command':'F'}).status_code)"
```

That should also return `302` when logged out.

## Phase Boundary

This phase includes authentication, camera viewing, backend serial command sending, and dashboard movement controls. Sensors, collection logic, telemetry, autonomous behavior, and advanced hardware integrations are not included.
