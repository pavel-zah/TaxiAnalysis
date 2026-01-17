from dataclasses import dataclass
from datetime import datetime


@dataclass
class Driver:
    """Сущность Водитель"""
    id: str
    username: str
    car_info: str
    register_date: datetime
