from typing import Any
from operator import itemgetter
from sqlalchemy_utils import Ltree
from datetime import date, datetime


class CastUtil:
    @staticmethod
    def cast(obj: Any, type_: Any) -> Any:
        """
        Try cast to some type

        :param obj: Any
        :param type_: Any
        :return: Any
        """

        try:
            obj = type_(obj)
        except TypeError:
            obj = None
        except ValueError:
            obj = None

        return obj

    @staticmethod
    def to_str(value: Any):
        """
        Try to get repr for datetime, date or Ltree

        :param value: Any (int, str, dict, list, Ltree, datetime, date)
        :return: representation value (int, str, dict, list)
        """

        if isinstance(value, datetime):
            value = value.strftime('%Y-%m-%d %H:%M:%S') if value else value

        elif isinstance(value, date):
            value = value.strftime('%Y-%m-%d') if value else value

        elif isinstance(value, Ltree):
            value = value.path

        elif isinstance(value, dict):
            value = dict(sorted(value.items(), key=itemgetter(0)))
            value = str(value)

        else:
            try:
                value = str(value)
            finally:
                pass

        return value
