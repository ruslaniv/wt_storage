import math
from typing import Self

from _decimal import Decimal

from src.models import Document
from src.settings.defaults import defaults as settings


class Calculator:
    def __init__(
        self,
        document: Document,
        writes: int = 1,
        reads: int = 2,
        number_of_users: int = 1_000_000,
    ):
        self.document = document
        self.writes = writes
        self.reads = reads
        self.number_of_users = number_of_users

    def calculate(self: Self):
        total_length_in_bytes = self._calculate_total_document_length()
        total_cost = self._calculate_requests_cost(total_length_in_bytes)
        return total_cost

    def _calculate_requests_cost(
        self: Self,
        total_length_in_bytes: int,
        strong_consistency: bool = True,
    ) -> Decimal:
        total_length_in_kilobytes = math.ceil(total_length_in_bytes / 1024)
        total_WRUs = total_length_in_kilobytes * self.number_of_users * self.writes
        if strong_consistency:
            total_RRUs = total_length_in_kilobytes * self.number_of_users * self.reads
        else:
            total_RRUs = (
                total_length_in_kilobytes * self.number_of_users * self.reads * 0.5
            )
        WRU_cost = total_WRUs * settings.WRU_COST
        RRU_cost = total_RRUs * settings.RRU_COST

        return WRU_cost + RRU_cost

    def _calculate_total_document_length(self: Self) -> int:
        document = self.document.model_json_schema()["properties"].keys()
        user_id_key_length, dt_key_length, activity_scores_key_length = (
            len(name.encode("utf-8")) for name in document
        )
        user_id_length = self._calculate_integer_length(self.document.u)
        dt_length = len(self.document.d.encode("utf-8"))
        activity_scores_length = len(self.document.s)
        overhead = settings.DYNAMODB_OVERHEAD
        return (
            user_id_key_length
            + user_id_length
            + dt_key_length
            + dt_length
            + activity_scores_key_length
            + activity_scores_length
            + overhead
        )

    @staticmethod
    def _calculate_integer_length(number: int) -> int:
        number_of_digits = len(str(number))
        base_storage_cost = (number_of_digits + 1) // 2
        total_storage_cost = base_storage_cost + 1
        return total_storage_cost
