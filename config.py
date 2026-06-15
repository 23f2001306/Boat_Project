from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"


class Config:
    SECRET_KEY = "change-this-secret-key-in-production"
    INSTANCE_DIR = INSTANCE_DIR
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{INSTANCE_DIR / 'boat_control.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CAMERA_INDEX = 0
    ARDUINO_BAUD_RATE = 9600
