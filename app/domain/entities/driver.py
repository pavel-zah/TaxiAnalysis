from dataclasses import dataclass
from datetime import datetime


@dataclass
class Driver:
    """Сущность Водитель"""
    id: str
    username: str
    license_plate: str
    register_date: datetime
