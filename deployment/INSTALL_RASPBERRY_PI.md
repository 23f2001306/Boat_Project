# Raspberry Pi Deployment Guide - Phase 8

This guide installs the Flask boat control system as a Gunicorn-powered systemd service that starts automatically on Raspberry Pi boot.

## Deployment Files

```text
Boat_Project/
|-- requirements.txt
|-- wsgi.py
`-- deployment/
    |-- boat-control.service
    |-- gunicorn.conf.py
    `-- INSTALL_RASPBERRY_PI.md
```

## 1. Install System Dependencies

On the Raspberry Pi:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip libgl1 libglib2.0-0
```

Optional but recommended for camera and Arduino access:

```bash
sudo usermod -aG video,dialout pi
```

Log out and back in after changing groups.

## 2. Copy Project To Raspberry Pi

Place the project at:

```text
/home/pi/Boat_Project
```

If you use a different path or Linux username, update these lines in `deployment/boat-control.service`:

```ini
User=pi
Group=pi
WorkingDirectory=/home/pi/Boat_Project
Environment="PATH=/home/pi/Boat_Project/venv/bin"
ExecStart=/home/pi/Boat_Project/venv/bin/gunicorn --config /home/pi/Boat_Project/deployment/gunicorn.conf.py wsgi:app
```

## 3. Create Virtual Environment

```bash
cd /home/pi/Boat_Project
python3 -m venv venv
source venv/bin/activate
```

## 4. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Initialize Database

The app creates the SQLite database automatically when the Flask app starts. To initialize it manually:

```bash
cd /home/pi/Boat_Project
source venv/bin/activate
python -c "from app import create_app; create_app(); print('Database initialized')"
```

The database will be created at:

```text
/home/pi/Boat_Project/instance/boat_control.db
```

## 6. Test With Gunicorn Manually

```bash
cd /home/pi/Boat_Project
source venv/bin/activate
gunicorn --config deployment/gunicorn.conf.py wsgi:app
```

Open from another device on the same network:

```text
http://RASPBERRY_PI_IP:5000
```

Stop the manual server with `Ctrl+C`.

## 7. Install systemd Service

```bash
cd /home/pi/Boat_Project
sudo cp deployment/boat-control.service /etc/systemd/system/boat-control.service
sudo systemctl daemon-reload
```

## 8. Start Application

```bash
sudo systemctl start boat-control
sudo systemctl status boat-control
```

## 9. Enable Startup On Boot

```bash
sudo systemctl enable boat-control
```

The app will now start automatically when the Raspberry Pi boots.

## 10. Optional Remote Command API

Browser control works after logging in from any device on the same network:

```text
http://RASPBERRY_PI_IP:5000
```

For direct command forwarding from scripts, microcontrollers, or other apps, set a shared API token in the systemd service:

```ini
Environment="BOAT_API_TOKEN=replace-with-a-long-random-token"
```

Then reload and restart:

```bash
sudo systemctl daemon-reload
sudo systemctl restart boat-control
```

Send commands to the Raspberry Pi with:

```bash
curl -X POST http://RASPBERRY_PI_IP:5000/api/remote-control \
  -H "Content-Type: application/json" \
  -H "X-Boat-Api-Key: replace-with-a-long-random-token" \
  -d '{"command":"F"}'
```

Valid commands are `F`, `B`, `L`, `R`, and `S`.

## 11. Useful Service Commands

Restart:

```bash
sudo systemctl restart boat-control
```

Stop:

```bash
sudo systemctl stop boat-control
```

View logs:

```bash
journalctl -u boat-control -f
```

Check enabled state:

```bash
systemctl is-enabled boat-control
```

## Notes

- Gunicorn listens on `0.0.0.0:5000`, so phones and laptops on the same network can open the app.
- The service waits for network startup with `network-online.target`.
- The service restarts automatically if the Flask/Gunicorn process exits.
- The configured Gunicorn worker count is `1` with `4` threads so camera and serial resources are not opened by multiple worker processes.
