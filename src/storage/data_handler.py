import gzip
import io
import pickle
from datetime import datetime, timedelta
from typing import MutableSequence, Self

from src.models import Document, User


class DataCompressor:
    @staticmethod
    def compress(data: MutableSequence[int]) -> bytes:
        with io.BytesIO() as bytes_io:
            with gzip.GzipFile(fileobj=bytes_io, mode="w") as gzip_file:
                gzip_file.write(pickle.dumps(data))
            return bytes_io.getvalue()


class DataHandler:
    def __init__(self, user: User, dt: datetime):
        self.user = user
        self.compressor = DataCompressor()
        self.date = dt

    def prepare_data_for_day(self: Self) -> Document | None:
        start_time = self.date.replace(
            hour=0, minute=0, second=0, microsecond=0
        ) - timedelta(days=1)
        end_time = start_time + timedelta(days=1)
        if not start_time <= self.user.dt <= end_time:
            raise ValueError("Invalid date")
        compressed_activity_scores = self.compressor.compress(self.user.activity_scores)

        user_data = {
            "u": self.user.user_id,
            "d": self.user.get_string_date(),
            "s": compressed_activity_scores,
        }

        return Document(**user_data)
