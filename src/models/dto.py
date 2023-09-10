from array import array
from collections.abc import MutableSequence
from typing import Annotated, Self

from pydantic import AfterValidator, AwareDatetime, BaseModel

__all__ = ["User", "Document"]

from src.validators.validators import validate_utc

DatetimeUTC = Annotated[AwareDatetime, AfterValidator(validate_utc)]


class Document(BaseModel):
    u: int
    d: str
    s: bytes


class User(BaseModel):
    user_id: int
    dt: DatetimeUTC
    activity_scores: MutableSequence[int] = array("H")
    # activity_scores: Annotated[list[int], AfterValidator(check_length_of_scores)]

    # @field_validator("activity_scores")
    # @classmethod
    # def convert_to_array(cls, v: list[int]) -> array:
    #     if isinstance(v, list):
    #         return array("H", v)
    #     elif isinstance(v, array):
    #         return v
    #     raise ValueError("Invalid data type for array")

    def get_string_date(self: Self) -> str:
        return self._date

    @property
    def _date(self: Self) -> str:
        return self.dt.strftime("%Y-%m-%d:%H:%M:%S")

    def __str__(self: Self) -> str:
        return f"Document for user: {self.user_id}, date:{self._date}, activity scores length: {len(self.activity_scores)})"

    def __repr__(self: Self) -> str:
        return f"Document(user_id={self.user_id}, date={self.dt}, activity_scores={self.activity_scores})"
