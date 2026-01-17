from dataclasses import dataclass
from datetime import datetime


@dataclass
class Driver:
    """Сущность Пользователь - пассажир"""
    id: str
    username: str
    register_date: datetime
