from abc import ABC, abstractmethod
from domain.entities.ride import Ride
from domain.entities.user import User
from domain.entities.driver import Driver


class DataGenerator(ABC):
    """Интерфейс для генерации данных о поездке, пользователе, водителе"""

    @abstractmethod
    def generate_ride(self, user_id, driver_id) -> Ride:
        """Сгенерировать объект поездки"""
        pass

    @abstractmethod
    def generate_user(self) -> User:
        """Сгенерировать объект пользователя"""
        pass

    @abstractmethod
    def generate_driver(self) -> Driver:
        """Сгенерировать объект водителя"""
        pass