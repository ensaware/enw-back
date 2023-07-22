from io import BytesIO

import cv2
import numpy as np
from PIL import Image
from pyzbar import pyzbar

from utils.quick_response_code import ReadQuickResponseCode


class BarCode(ReadQuickResponseCode):
    def read(self, image: bytes) -> str:
        barcode_img = Image.open(BytesIO(image))
        gray_img = cv2.cvtColor(np.array(barcode_img), cv2.COLOR_BGR2GRAY)
        codes = pyzbar.decode(gray_img)

        detected_codes = []
        for code in codes:
            data = code.data.decode("utf-8")
            _type = code.type

            detected_codes.append({"type": _type, "data": data})

        return detected_codes[0]['data']