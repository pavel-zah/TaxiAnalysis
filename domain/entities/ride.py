from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Ride:
    """Сущность Поездка"""
    id: str
    driver_id: str
    rider_id: str
    starting_point: str
    destination: str
    started_at: datetime
    ended_at: datetime | None # равно None, если поездка не была совершена или еще в процессе
    finished: bool
    ride_time: int
    price: Decimal = Decimal("0.00")
    tip: Decimal = Decimal("0.00")


    @property
    def ride_time(self) -> int:
        """Время поездки в минутах. Равняется 0 если поезда не была совершена"""
        if self.ended_at == None and self.finished == True: return 0

        seconds = (self.ended_at - self.started_at).total_seconds()
        minutes = int(seconds // 60)
        return minutes
