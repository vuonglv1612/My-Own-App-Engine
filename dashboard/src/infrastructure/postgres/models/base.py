from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import MetaData

from src.utils.datetime import aware_to_naive, naive_to_aware

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
