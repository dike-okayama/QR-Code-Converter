#!python3.10
# -*- coding: utf-8 -*-

from io import BytesIO
import base64
import datetime

import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import qrcode
import cv2
from PIL import Image

app = Flask(__name__)
qcd = cv2.QRCodeDetector()

logo = Image.open("backend/static/favicon.png").resize((60, 60))

CORS(app, supports_credentials=True)


class QRImage:
    @staticmethod
    def to_bytes(text: str) -> bytes:
        with BytesIO() as stream:
            qrcode.make(
                text, border=2, error_correction=qrcode.constants.ERROR_CORRECT_H
            ).save(stream, "PNG")
            stream.seek(0)
            return stream.read()

    @classmethod
    def to_b64(cls, text: str) -> bytes:
        return base64.b64encode(cls.to_bytes(text)).decode("utf-8")


def logger(func):
    def wrapper(*args, **kwargs):
        with open("backend/log.txt", mode="a+") as f:
            f.write(str(datetime.datetime.now()) + "\n")
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


@app.route("/url-to-qrcode", methods=["GET"])
@logger
def url_to_qrcode():
    url = request.args.get("url")
    b64 = QRImage.to_b64(url)
    img = Image.open(BytesIO(base64.b64decode((b64))))
    img.paste(logo, box=(95, 95))
    with BytesIO() as stream:
        img.save(stream, format="PNG")
        img_str = base64.b64encode(stream.getvalue()).decode("utf-8")
    return jsonify(dict(qrcode=img_str))


@app.route("/qrcode-to-url", methods=["GET"])
@logger
def qrcode_to_url():
    img_b64 = request.args.get("qrcode").replace(" ", "+")
    src = cv2.imdecode(
        np.frombuffer(base64.b64decode(img_b64), np.uint8), cv2.IMREAD_GRAYSCALE
    )
    return jsonify(dict(url=qcd.detectAndDecodeMulti(src)[1][0]))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
