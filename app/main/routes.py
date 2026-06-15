from flask import Blueprint, Response, current_app, jsonify, redirect, render_template, request, url_for
from flask_login import login_required

from app.camera import VideoCamera, generate_mjpeg
from app.serial_controller import ArduinoService


main_bp = Blueprint("main", __name__)
camera = VideoCamera()
arduino = ArduinoService()


@main_bp.route("/")
def index():
    return redirect(url_for("auth.login"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    camera.camera_index = current_app.config["CAMERA_INDEX"]
    return render_template("dashboard.html", camera_status=camera.get_status())


@main_bp.route("/video_feed")
@login_required
def video_feed():
    camera.camera_index = current_app.config["CAMERA_INDEX"]
    return Response(
        generate_mjpeg(camera),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@main_bp.route("/camera_status")
@login_required
def camera_status():
    camera.camera_index = current_app.config["CAMERA_INDEX"]
    return jsonify(camera.get_status())


@main_bp.route("/api/test-command", methods=["POST"])
@login_required
def test_command():
    return send_arduino_command()


@main_bp.route("/api/control", methods=["POST"])
@login_required
def control():
    return send_arduino_command()


def send_arduino_command():
    arduino.baud_rate = current_app.config["ARDUINO_BAUD_RATE"]
    data = request.get_json(silent=True) or {}
    result = arduino.send_command(data.get("command"))
    status_code = 200 if result["success"] else 400
    return jsonify(result), status_code
