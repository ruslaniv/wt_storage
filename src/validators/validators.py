from datetime import timezone

from pydantic import AwareDatetime

from src.settings.defaults import defaults as settings

__all__ = [
    "check_length_of_scores",
    "validate_utc",
]


def check_length_of_scores(scores: list[int]) -> list[int]:
    assert (
        len(scores) == settings.MEASUREMENTS_PER_DAY
    ), f"{len(scores)} must be equal to {settings.MEASUREMENTS_PER_DAY}"
    return scores


def validate_utc(dt: AwareDatetime) -> AwareDatetime:
    if dt.tzinfo.utcoffset(dt) != timezone.utc.utcoffset(dt):
        raise ValueError("Timezone must be UTC")
    return dt
