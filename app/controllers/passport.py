import json
import numpy as np

from PIL import Image
from aiohttp import web
from io import BytesIO
from orion_api import OrionApi
from .base import BaseController
from scanner import DocumentScanner
from utils.image_utils import ImageUtils


class PassportScanningController(BaseController):
    @classmethod
    async def get_contours(cls, request: web.Request):
        """
        @api {get} /contours/passport Получение контура паспорта с изображения
        @apiName GetPassportContours
        @apiGroup Passport
        @apiVersion 0.0.1
        @apiDescription НЕ ГОТОВА! В РАЗРАБОТКЕ

        @apiSuccessExample Ответ сервера
            {

            }
        """
        pass

    @classmethod
    async def post(cls, request: web.Request):
        """
        @api {post} /scanning/passport Получение данных с изображения паспорта
        @apiName ScanningPassport
        @apiGroup Passport
        @apiVersion 0.0.1
        @apiDescription Распазнает данные на изображении паспорта, на вход может принять координаты паспорта (полученные в api по контурам)

        @apiHeader (Заголовки) {String} Content-Type multipart/form-data

        @apiParam (form-data) {Object} attachment Изображение паспорта
        @apiParam (form-data) {Object} payload Данные в JSON формате, например, контур паспорта

        @apiParamExample {json} Пример данных в ключе payload
            {
                "contours": [[43, 56], [34, 567], [234, 546], [234, 23]]
            }

        @apiSuccessExample Ответ сервера
            {
                "passport_data": {
                        "full_name": "Мартиника Константиновна Фрай",
                        "date_of_birth": "15.05.1995",
                        "date_of_issue": "06.06.2006",
                        "place_of_birth": "Село Сайлем",
                        "name_issue_department": "Иепархия св. Петра",
                        "number_issue_department": "666-666",
                        "serial_number": "00 00 000000"
                }
            }
        """

        data = await request.post()

        received_body = data.get('payload')
        received_body = json.loads(received_body)

        file_field = data.get('attachment')
        img_content = file_field.file.read()

        image = Image.open(BytesIO(img_content))
        image = ImageUtils.get_np_array_of_image(image)

        contours = received_body.get('contours')
        if contours:
            contours = np.array(contours)

        data = {
            'contours': contours,
            'filename': file_field.filename,
            'image': image
        }

        document_scanner = DocumentScanner(data, 'passport')
        passport_data = await document_scanner.execute_scanning()

        data = {
            'attributes': passport_data,
            'type': 'ocr/passport'
        }
        return OrionApi().serialize_json(data).response
