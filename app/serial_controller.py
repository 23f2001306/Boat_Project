import threading
import time

try:
    import serial
    from serial.tools import list_ports
except ImportError:
    serial = None
    list_ports = None


class ArduinoService:
    VALID_COMMANDS = {"F", "B", "L", "R", "S"}
    ARDUINO_KEYWORDS = ("arduino", "ch340", "wch", "usb serial", "usb-serial")

    def __init__(self, baud_rate=9600, timeout=1):
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.connection = None
        self.port = None
        self.last_error = "Arduino is not connected."
        self.lock = threading.Lock()

    def detect_port(self):
        if list_ports is None:
            self.last_error = "PySerial is not installed."
            return None

        ports = list(list_ports.comports())
        for port in ports:
            details = " ".join(
                str(value).lower()
                for value in (port.description, port.manufacturer, port.hwid)
                if value
            )
            if any(keyword in details for keyword in self.ARDUINO_KEYWORDS):
                return port.device

        if len(ports) == 1:
            return ports[0].device

        self.last_error = "No Arduino serial port detected."
        return None

    def connect(self):
        if serial is None:
            self.last_error = "PySerial is not installed."
            return False

        if self.connection is not None and self.connection.is_open:
            return True

        self.disconnect()
        detected_port = self.detect_port()
        if detected_port is None:
            return False

        try:
            self.connection = serial.Serial(
                detected_port,
                self.baud_rate,
                timeout=self.timeout,
                write_timeout=self.timeout,
            )
            time.sleep(2)
            self.port = detected_port
            self.last_error = None
            return True
        except serial.SerialException as exc:
            self.connection = None
            self.port = None
            self.last_error = f"Could not connect to Arduino: {exc}"
            return False

    def disconnect(self):
        if self.connection is not None:
            try:
                self.connection.close()
            except serial.SerialException:
                pass
        self.connection = None
        self.port = None

    def get_status(self):
        with self.lock:
            connected = self.connection is not None and self.connection.is_open
            if not connected and self.port is not None:
                self.last_error = "Arduino disconnected."
                self.disconnect()

            return {
                "connected": connected,
                "port": self.port,
                "baud_rate": self.baud_rate,
                "message": "Arduino connected." if connected else self.last_error,
            }

    def send_command(self, command):
        command = str(command or "").strip().upper()

        if command not in self.VALID_COMMANDS:
            return {
                "success": False,
                "sent": False,
                "command": command,
                "message": "Invalid command. Use one of: F, B, L, R, S.",
            }

        with self.lock:
            if not self.connect():
                return {
                    "success": False,
                    "sent": False,
                    "command": command,
                    "message": self.last_error,
                }

            try:
                self.connection.write(command.encode("utf-8"))
                self.connection.flush()
                return {
                    "success": True,
                    "sent": True,
                    "command": command,
                    "port": self.port,
                    "message": f"Command {command} sent to Arduino.",
                }
            except serial.SerialException as exc:
                self.last_error = f"Arduino disconnected while sending command: {exc}"
                self.disconnect()
                return {
                    "success": False,
                    "sent": False,
                    "command": command,
                    "message": self.last_error,
                }
