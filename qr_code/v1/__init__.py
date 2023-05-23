from io import BytesIO
import json
import logging
from os import remove, path
from uuid import uuid4

import cv2
from fastapi import status
import pyqrcode
from PIL import Image
from sqlalchemy.orm import Session

from exception import Error, TypeMessage, Validate
from exception.ensaware import EnsawareException
from user.v1.crud import get_user_id
from user.v1.schema import TokenData
from utils.encryption import Encryption


from . import crud, schema


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


    def generate(self, id: str, show_logo: bool, background: str = None, color: str = None) -> bytes:
        user = get_user_id(self._db, id)
        if not(user):
            raise EnsawareException(status.HTTP_400_BAD_REQUEST, TypeMessage.VALIDATION.value, Validate.INVALID_USER.value)
        
        historic_qr_code = crud.create_historic_qr_code(self._db, user.id)

        user_history = schema.UserHistory(
            career_id=user.career_id,
            email=user.email,
            id=historic_qr_code.id,
            name=user.display_name,
            user_id=user.id,
        )

        json_object = json.dumps(user_history.dict(), indent=4)
    
        token: str = self._encryption.encrypt(json_object)
        name_img_qr: str = self.__create(token, background, color)

        try:
            image_qr: Image.Image = self.__open_image(name_img_qr)

            if show_logo:
                logo_cua: Image.Image = self.__open_image('logo-cua.png').resize((150, 150))
                image_qr.paste(logo_cua, self.__get_position(image_qr, logo_cua), logo_cua)

            buffered: BytesIO = BytesIO()
            image_qr.save(buffered, format='PNG')

            return buffered.getvalue()
        except Exception as ex:
            logging.exception(ex)
            raise EnsawareException(status.HTTP_400_BAD_REQUEST, TypeMessage.VALIDATION.value, Validate.INVALID_USER.value)
        finally:
            if path.exists(name_img_qr):
                remove(name_img_qr)
    

    def read(self, toke_data: TokenData, token: str) -> schema.UserHistory:
        try:
            decrypt: str = self._encryption.decrypt(token)
            data = json.loads(decrypt)
            user_history = schema.UserHistory(**data)

            qr_data = crud.get_historic_qr_code_id(self._db, user_history.id)

            if not(qr_data):
                raise EnsawareException(status.HTTP_400_BAD_REQUEST, TypeMessage.ERROR.value, Error.QR_CODE_READ.value)
            
            if qr_data.user_id != toke_data.sub:
                raise EnsawareException(status.HTTP_401_UNAUTHORIZED, TypeMessage.ERROR.value, Error.QR_CODE_AUTH.value)
            
            return user_history
        except EnsawareException as enw:
            logging.exception(enw)
            raise enw
        except Exception as ex:
            logging.exception(ex)
            raise EnsawareException(status.HTTP_400_BAD_REQUEST, TypeMessage.ERROR.value, Error.QR_CODE_READ.value)
    

    def read_image(self, image: bytes) -> str:
        code_detector = cv2.QRCodeDetector()
        file_name = f'{str(uuid4())}.png'

        try:
            img: Image.Image = Image.open(BytesIO(image))
            img.save(file_name)
            qr = cv2.imread(file_name)
            token, _, _ = code_detector.detectAndDecode(qr)

            return token
        except Exception as ex:
            logging.exception(ex)
            raise EnsawareException(status.HTTP_400_BAD_REQUEST, TypeMessage.ERROR.value, Error.QR_CODE_READ.value)
        finally:
            if path.exists(file_name):
                remove(file_name)