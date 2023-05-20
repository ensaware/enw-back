from io import BytesIO
from os import remove, path
from uuid import uuid4

import cv2
import pyqrcode
from PIL import Image
from sqlalchemy.orm import Session

from exception.qr import Error, QRCodeError, QRCodeValidate, Validate
from . import crud, models

from utils.encryption import Encryption


class QR:
    def __init__(self, db: Session) -> None:
        self._db: Session = db
        self._encryption: Encryption = Encryption()


    def __open_image(self, path: str) -> Image.Image:
        return Image.open(path).convert('RGBA')


    def __create(self, message: str, background: str = None, color: str = None) -> str:
        name_qr: str = f'{str(uuid4())}.png'
        scale: int = 10

        qr = pyqrcode.create(message, error='H')

        if not(color):
            color = '#181818'

        if not(background):
            background = '#FBFBFB'

        qr.png(name_qr, scale=scale, background=background, module_color=color)

        return name_qr
    

    def __get_position(self, qr_image: Image.Image, logo: Image.Image) -> tuple[int, int]:
        return (
                    (qr_image.size[0] - logo.size[0]) // 2, 
                    (qr_image.size[1] - logo.size[1]) // 2
                )


    def generate(self, email: str, url: str, show_logo: bool, background: str = None, color: str = None) -> bytes:
        qr_email: models.QRCode = crud.get_qr_code_email(
            self._db,
            email
        )

        if not(qr_email):
            raise QRCodeValidate(Validate.INVALID_EMAIL)
    
        encrypt: str = self._encryption.encrypt(qr_email.id)
        url: str = f'{url}api/v1/qr-code/{email}/read?token={encrypt}'
        name_img_qr: str = self.__create(url, background, color)

        try:
            image_qr: Image.Image = self.__open_image(name_img_qr)

            if show_logo:
                logo_cua: Image.Image = self.__open_image('logo-cua.png').resize((150, 150))
                image_qr.paste(logo_cua, self.__get_position(image_qr, logo_cua), logo_cua)

            buffered: BytesIO = BytesIO()
            image_qr.save(buffered, format='PNG')

            return buffered.getvalue()
        finally:
            if path.exists(name_img_qr):
                remove(name_img_qr)
    

    def read(self, email: str, token: str) -> models.QRCode:
        decrypt: str = self._encryption.decrypt(token)
        qr_id: models.QRCode = crud.get_qr_code(self._db, decrypt)

        if not(qr_id):
            raise QRCodeError(Error.READ_QR_CODE)

        if qr_id.email.lower() != email.lower():
            raise QRCodeError(Error.READ_QR_CODE)
        
        return qr_id
    

    def read_imagen(self, email: str, image: bytes) -> models.QRCode:
        code_detector = cv2.QRCodeDetector()
        file_name = f'{str(uuid4())}.png'

        try:
            img: Image.Image = Image.open(BytesIO(image))
            img.save(file_name)
            qr = cv2.imread(file_name)
            token, _, _ = code_detector.detectAndDecode(qr)
            
            index = token.index("token=")
            token = token[index: len(token)].replace('token=', '')

            return self.read(email, token)
        finally:
            if path.exists(file_name):
                remove(file_name)