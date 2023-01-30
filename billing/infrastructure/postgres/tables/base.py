import json
from datetime import datetime

import sqlalchemy as sa
from attrs import asdict
from sqlalchemy import MetaData

from utils.datetime import aware_to_naive, naive_to_aware

metadata = MetaData()


class TimeStamp(sa.types.TypeDecorator):
    impl = sa.types.DateTime

    def process_bind_param(self, value, dialect):
        if isinstance(value, datetime):
            return aware_to_naive(value)
        else:
            return value

    def process_result_value(self, value, dialect):
        if isinstance(value, datetime):
            return naive_to_aware(value)
        else:
            return value


def _default(val):
    if hasattr(val, '__attrs_attrs__'):
        return asdict(val)
    if isinstance(val, datetime):
        return val.isoformat()
    raise TypeError()


def custom_json_serializer(d):
    return json.dumps(d, default=_default)
