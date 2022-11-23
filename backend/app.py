#!python3.10
# -*- coding: utf-8 -*-

from io import BytesIO
import base64

import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import qrcode
import cv2


app = Flask(__name__)
qcd = cv2.QRCodeDetector()


CORS(
    app,
    supports_credentials=True
)


class QRImage():

    @staticmethod
    def to_bytes(text: str) -> bytes:
        with BytesIO() as stream:
            qrcode.make(text,
                        border=2).save(stream, 'PNG')
            stream.seek(0)
            return stream.read()

    @classmethod
    def to_b64(cls, text: str) -> bytes:
        return base64.b64encode(cls.to_bytes(text))\
                     .decode("utf-8")


@app.route('/url-to-qrcode', methods=['GET'])
def url_to_qrcode():
    url = request.args.get('url')
    return jsonify(dict(qrcode=QRImage.to_b64(url)))


@app.route('/qrcode-to-url', methods=['GET'])
def qrcode_to_url():
    img_b64 = request.args.get('qrcode').replace(' ', '+')
    src = cv2.imdecode(np.frombuffer(base64.b64decode(img_b64),
                                     np.uint8),
                       cv2.IMREAD_GRAYSCALE)
    return jsonify(dict(url=qcd.detectAndDecodeMulti(src)[1][0]))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
