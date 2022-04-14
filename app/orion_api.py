import enum

from aiohttp import web_exceptions


class ResponseType(enum.Enum):
    error = 0
    attachment = 1
    orion_api = 2
    custom_json = 3
    http_code = 4
    text = 5


class OrionApi:
    _response_subclasses = [
        *web_exceptions.HTTPServerError.__subclasses__(),
        *web_exceptions.HTTPClientError.__subclasses__(),
        *web_exceptions.HTTPSuccessful.__subclasses__()
    ]

    http_responses = {resp.status_code: resp for resp in _response_subclasses if getattr(resp, 'status_code', None)}

    def __init__(self):
        self._meta = {}
        self._data = {}
        self._error = {}
        self._included = []
        self._http_code = 200
        self._attachment = None
        self._is_collection = None
        self.response_type = None
        self._database_entities = None

    @property
    def response(self) -> dict:
        """
        Collect data, meta and included in json and return it

        :return:
        """

        if self.response_type == ResponseType.error.value:
            result = self._error

        elif self.response_type == ResponseType.custom_json.value:
            self._meta = {}
            self._included = []

            result = {
                'meta': self._meta,
                'data': self._data,
                'included': self._included
            }

        else:
            self.empty_object()

            result = {
                'meta': self._meta,
                'data': self._data,
                'included': self._included
            }

        return result

    def empty_object(self) -> 'OrionApi':
        """
        Initialize instance as empty OrionApi object where data is dict

        :return: Any
        """

        self._meta = {}
        self._data = {}
        self._included = []
        self._database_entities = None

        self._is_collection = False
        self.response_type = ResponseType.orion_api.value

        return self

    def serialize_json(self, json_data: dict) -> 'OrionApi':
        """
        Packs json(dict) in OrionApi class

        :param json_data:
        :return:
        """

        self._data = json_data
        self.response_type = ResponseType.custom_json.value

        return self
