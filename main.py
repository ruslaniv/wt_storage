from datetime import datetime, timezone

from src.factories.factory import FakeDailyActivity
from src.models.dto import Document, User
from src.storage.data_handler import DataHandler
from src.utils.cost_estimator import Calculator

daily_activities = FakeDailyActivity(yesterday=True, number_of_users=3).create()


def convert_to_dynamodb_documents(users: list[User], dt: datetime) -> list[Document]:
    data = []
    dt_utc = dt.astimezone(timezone.utc)
    for user in users:
        handler = DataHandler(user, dt_utc)
        data.append(handler.prepare_data_for_day())
    return data


def estimate_cost(data: list[Document]) -> None:
    costs = []
    for document in data:
        calculator = Calculator(document)
        cost = calculator.calculate()
        costs.append(cost)
    print(f"${sum(costs):.2f}")


estimate_cost(convert_to_dynamodb_documents(daily_activities, datetime.now()))
