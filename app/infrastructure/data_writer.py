import psycopg2
from typing import List
from app.domain.entities.user import User
from app.domain.entities.driver import Driver
from app.domain.entities.ride import Ride


class DBWriter:
    """Класс для записи данных об объектах в Postgres"""
    def __init__(self, host, port, database):

        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user='user',
            password='password123'
        )

    def create_user_batch(self, users: List[User]):
        """Метод для записи данных об пользователях в Postgres"""
        with self.conn.cursor() as cursor:
            for user in users:
                cursor.execute(
                    """
                    INSERT INTO users (id, username, register_date)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        user.id,
                        user.username,
                        user.register_date
                    )
                )
        self.conn.commit()

    def create_driver_batch(self, drivers: List[Driver]):
        """Метод для записи данных о водителях в Postgres"""

        with self.conn.cursor() as cursor:
            for driver in drivers:
                cursor.execute(
                    """
                    INSERT INTO drivers (id, username, license_plate, register_date)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        driver.id,
                        driver.username,
                        driver.license_plate,
                        driver.register_date
                    )
                )
        self.conn.commit()

    def create_ride_batch(self, rides: List[Ride]):
        """Метод для записи данных о поездке в Postgres"""

        with self.conn.cursor() as cursor:
            for ride in rides:
                cursor.execute(
                    """
                    INSERT INTO rides (id, driver_id, rider_id, starting_point, destination, started_at, ended_at, price, tip)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        ride.id,
                        ride.driver_id,
                        ride.rider_id,
                        ride.starting_point,
                        ride.destination,
                        ride.started_at,
                        ride.ended_at,
                        ride.price,
                        ride.tip
                    )
                )
        self.conn.commit()

    def close(self):
        self.conn.close()