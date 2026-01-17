from abc import ABC, abstractmethod
from domain.entities.ride import Ride
from domain.entities.user import User




class DataGenerator(ABC):
    """Интерфейс для генерации данных о поездке, пользователе, водителе"""

    @abstractmethod
    def generateRide(self) -> Ride:
        """Сгенерировать уникальный ID"""
        pass