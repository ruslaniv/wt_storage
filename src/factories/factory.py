import random
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from random import randint
from typing import Any, Self

import pytz
from faker import Faker

from src.models import User
from src.settings.defaults import defaults as settings

fake = Faker()

Faker.seed(settings.RANDOM_SEED)
random.seed(settings.RANDOM_SEED)

__all__ = ["FakeUserFactory", "FakeDailyActivity"]


class Fake(ABC):
    @abstractmethod
    def create(self: Self) -> Any:
        raise NotImplementedError


class FakeUserFactory(Fake):
    def __init__(self: Self, yesterday: bool = True) -> None:
        self.user_id: int = randint(1, 1_000_000 + 1)
        self.dt: datetime = fake.date_time(tzinfo=pytz.utc)
        self.activity_scores: list[int] = [
            randint(1, 100 + 1) for _ in range(settings.MEASUREMENTS_PER_DAY)
        ]
        if yesterday:
            self.dt = datetime.now().astimezone(timezone.utc) - timedelta(days=1)

    def create(self: Self) -> User:
        return User(
            user_id=self.user_id, dt=self.dt, activity_scores=self.activity_scores
        )


class FakeDailyActivity(Fake):
    def __init__(self: Self, number_of_users: int = 1, yesterday: bool = True) -> None:
        self.number_of_users = number_of_users
        self.yesterday = yesterday

    def create(self: Self) -> list[User]:
        daily_activities = [
            FakeUserFactory(yesterday=self.yesterday).create()
            for _ in range(self.number_of_users)
        ]
        return daily_activities
