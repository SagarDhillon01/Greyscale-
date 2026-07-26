import io
import os
import socket
from typing import Optional

import cv2
import numpy as np


def convert_to_grayscale(image_path: str, output_path: str) -> None:
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not read image from {image_path}")

    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    success = cv2.imwrite(output_path, grayscale_image)
    if not success:
        raise OSError(f"Could not write grayscale image to {output_path}")


def convert_to_grayscale_bytes(image_bytes: bytes) -> bytes:
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("The uploaded file is not a valid image")

    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, encoded_image = cv2.imencode(".jpg", grayscale_image)
    return encoded_image.tobytes()


def get_available_port(start_port: int) -> int:
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("0.0.0.0", port))
                return port
            except OSError:
                port += 1


def build_simple_web_app() -> None:
    from flask import Flask, request, send_file

    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index() -> Optional[object]:
        if request.method == "POST":
            if "image" not in request.files:
                return "No file uploaded", 400

            uploaded_file = request.files["image"]
            if uploaded_file.filename == "":
                return "No file selected", 400

            try:
                grayscale_bytes = convert_to_grayscale_bytes(uploaded_file.read())
            except ValueError as exc:
                return str(exc), 400

            return send_file(
                io.BytesIO(grayscale_bytes),
                mimetype="image/jpeg",
                as_attachment=True,
                download_name="grayscale.jpg",
            )

        return """
        <h1>Simple Grayscale Converter</h1>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*" required>
            <button type="submit">Convert to grayscale</button>
        </form>
        """

    requested_port = int(os.environ.get("PORT", 5000))
    port = get_available_port(requested_port)
    if port != requested_port:
        print(f"Port {requested_port} is busy; using {port} instead.")

    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    build_simple_web_app()