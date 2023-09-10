from _decimal import Decimal


class Defaults:
    def __init__(self):
        self.RANDOM_SEED = 42
        self._hours = 24
        self._minutes = 60
        self._seconds = 60
        self.FREQUENCY = 30
        self.MEASUREMENTS_PER_DAY = (
            self._hours * self._minutes * self._seconds // self.FREQUENCY
        )
        self.DYNAMODB_OVERHEAD = 100
        self.WRU_COST = Decimal(1.25) / 1_000_000
        self.RRU_COST = Decimal(0.25) / 1_000_000


defaults = Defaults()
