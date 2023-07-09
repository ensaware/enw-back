from io import BytesIO
import json
import logging
from os import remove, path
from uuid import uuid4

import cv2
from fastapi import status
from PIL import Image
import pyqrcode
from sqlalchemy.orm import Session

from . import CreateQuickResponseCode, ReadQuickResponseCode
from qr_code.v1.crud import create_historic_qr_code, get_historic_qr_code_id, update_historic_qr_code_id
from qr_code.v1.schema import HistoricQrCode
from user.v1.crud import get_user_id
from utils.encryption import Encryption
from utils.exception import Error, TypeMessage, Validate
from utils.exception.ensaware import EnsawareException


class QRCode(CreateQuickResponseCode, ReadQuickResponseCode):
    def __init__(self, db: Session, user_id: str, background: str = None, color: str = None, show_cua_logo: bool = False) -> None:
        self.__background = background
        self.__color = color
        self.__db = db
        self.__encryption: Encryption = Encryption()
        self.__show_cua_logo = show_cua_logo
        self.__user_id = user_id


    def __get_position(self, qr_image: Image.Image, cua_logo: Image.Image) -> tuple[int, int]:
        qr_width, qr_height = qr_image.size
        cua_logo_width, cua_logo_height = cua_logo.size

        return (
            (qr_width - cua_logo_width) // 2,
            (qr_height - cua_logo_height) // 2
        )


    def __get_token(self) -> str:
        user = get_user_id(self.__db, self.__user_id)
        if not(user):
            raise EnsawareException(status.HTTP_400_BAD_REQUEST, TypeMessage.VALIDATION.value, Validate.INVALID_USER.value)
        
        historic_qr_code = create_historic_qr_code(self.__db, user.id, True)
        data: dict = {
            'career_id': user.career_id,
            'email': user.email,
            'id': historic_qr_code.id,
            'name': user.display_name,
            'user_id': user.id,
        }
        json_object = json.dumps(data, indent=4)
        token: str = self.__encryption.encrypt(json_object)

        historic_qr_code.data = token
        update_historic_qr_code_id(self.__db, historic_qr_code.id, historic_qr_code)

        return token
    

    def __open(self, path: str) -> Image.Image:
        return Image.open(path).convert('RGBA')
    

    def __save(self, token: str) -> str:
        name_qr: str = f'{str(uuid4())}.png'
        scale: int = 10

        qr = pyqrcode.create(token, error='H')

        if not(self.__background):
            background = '#FBFBFB'

        if not(self.__color):
            color = '#181818'

        qr.png(name_qr, scale=scale, background=background, module_color=color)

        return name_qr

    
    def create(self) -> bytes:
        img_qr: str = self.__save(self.__get_token())
        
        try:
            image_qr: Image.Image = self.__open(img_qr)

            if self.__show_cua_logo:
                cua_logo: Image.Image = self.__open(f'{path.dirname(__file__)}/logo-cua.png').resize((150, 150))
                image_qr.paste(cua_logo, self.__get_position(image_qr, cua_logo), cua_logo)

            buffered: BytesIO = BytesIO()
            image_qr.save(buffered, format='PNG')

            return buffered.getvalue()
        except Exception as ex:
            logging.exception(ex)
            raise EnsawareException(status.HTTP_400_BAD_REQUEST, TypeMessage.VALIDATION.value, Validate.INVALID_QR_CODE_CREATE.value)
        finally:
            if path.exists(img_qr):
                remove(img_qr)


    def read(self, image: bytes) -> HistoricQrCode:
        code_detector = cv2.QRCodeDetector()
        file_name = f'{str(uuid4())}.png'

        try:
            qr_image: Image.Image = Image.open(BytesIO(image))
            qr_image.save(file_name)
            qr_data = cv2.imread(file_name)
            token, _, _ = code_detector.detectAndDecode(qr_data)


            decrypt: str = self.__encryption.decrypt(token)
            data: dict = json.loads(decrypt)
            
            qr_data = get_historic_qr_code_id(self.__db, data.get('id', None))

            if not(qr_data):
                raise EnsawareException(status.HTTP_400_BAD_REQUEST, TypeMessage.ERROR.value, Error.QR_CODE_READ.value)

            return qr_data
        except Exception as ex:
            logging.exception(ex)
            raise EnsawareException(status.HTTP_400_BAD_REQUEST, TypeMessage.ERROR.value, Error.QR_CODE_READ.value)
        finally:
            if path.exists(file_name):
                remove(file_name)