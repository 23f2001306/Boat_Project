import base64
import threading
import time

try:
    import cv2
    import numpy as np
except ImportError:
    cv2 = None
    np = None


OFFLINE_JPEG = base64.b64decode(
    "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////"
    "2wBDAf//////////////////////////////////////////////////////////////////////////////////////"
    "wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAX/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/"
    "9oADAMBAAIQAxAAAAH/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/9oACAEBAAEFAqf/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/"
    "9oACAEDAQE/ASP/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oACAECAQE/ASP/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/"
    "9oACAEBAAY/Ar//xAAUEAEAAAAAAAAAAAAAAAAAAAAA/9oACAEBAAE/IV//2gAMAwEAAgADAAAAEP/EABQRAQAAAAAAAAAAAAAAAAAAABD/"
    "2gAIAQMBAT8QP//EABQRAQAAAAAAAAAAAAAAAAAAABD/2gAIAQIBAT8QP//EABQQAQAAAAAAAAAAAAAAAAAAABD/2gAIAQEAAT8QP//Z"
)


class VideoCamera:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.capture = None
        self.connected = False
        self.last_error = "Camera has not been opened."
        self.lock = threading.Lock()

    def open(self):
        if cv2 is None:
            self.connected = False
            self.last_error = "OpenCV is not installed."
            return False

        if self.capture is not None and self.capture.isOpened():
            self.connected = True
            self.last_error = None
            return True

        self.release()
        self.capture = cv2.VideoCapture(self.camera_index)

        if not self.capture.isOpened():
            self.connected = False
            self.last_error = f"Unable to open camera index {self.camera_index}."
            self.release()
            return False

        self.connected = True
        self.last_error = None
        return True

    def release(self):
        if self.capture is not None:
            self.capture.release()
        self.capture = None

    def get_status(self):
        with self.lock:
            if cv2 is None:
                self.connected = False
                self.last_error = "OpenCV is not installed."
            elif self.capture is not None and not self.capture.isOpened():
                self.connected = False
                self.last_error = "Camera disconnected."
                self.release()

            return {
                "connected": self.connected,
                "camera_index": self.camera_index,
                "message": "Camera connected." if self.connected else self.last_error,
            }

    def get_frame(self):
        with self.lock:
            if not self.open():
                return self._offline_frame()

            success, frame = self.capture.read()
            if not success:
                self.connected = False
                self.last_error = "Camera disconnected or frame could not be read."
                self.release()
                return self._offline_frame()

            success, encoded_frame = cv2.imencode(".jpg", frame)
            if not success:
                self.connected = False
                self.last_error = "Frame could not be encoded."
                return self._offline_frame()

            self.connected = True
            self.last_error = None
            return encoded_frame.tobytes()

    def _offline_frame(self):
        if cv2 is None or np is None:
            return OFFLINE_JPEG

        frame = np.zeros((360, 640, 3), dtype=np.uint8)
        cv2.putText(
            frame,
            "Camera Offline",
            (170, 175),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            frame,
            "Check camera connection",
            (170, 220),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (180, 180, 180),
            2,
            cv2.LINE_AA,
        )
        success, encoded_frame = cv2.imencode(".jpg", frame)
        return encoded_frame.tobytes() if success else OFFLINE_JPEG


def generate_mjpeg(camera):
    while True:
        frame = camera.get_frame()
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        )
        time.sleep(0.05)
