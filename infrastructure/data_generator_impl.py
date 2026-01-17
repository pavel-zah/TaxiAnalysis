from domain.services.data_generator import DataGenerator
from domain.entities.ride import Ride
from domain.entities.user import User
from domain.entities.driver import Driver
from datetime import datetime, timedelta
import random
from faker import Faker
from decimal import Decimal, getcontext

getcontext().prec = 2

def gen_datetime(min_year=2020, max_year=datetime.now().year) -> datetime:
    """ генерирует datetime в формате yyyy-mm-dd hh:mm:ss.000000 """
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()


def gen_ride_end_time(ride_start: datetime, duration_minutes) -> datetime:
    """ создает datetime - время конца поездки """
    ride_duration = timedelta(minutes=duration_minutes)
    return ride_start + ride_duration


class FakeDataGenerator(DataGenerator):
    """Класс для создания фейковых данных"""

    def __init__(self, model_name="qwen/qwen3-vl-4b"):
        self.fake = Faker("ru_RU")

    def generate_ride(self, user_id, driver_id) -> Ride:
        """Сгенерировать объект поездки"""
        ride_id = str(random.randint(1_000_000_000_000_000, 10_000_000_000_000_000 - 1))
        starting_point = self.fake.street_address()
        destination = self.fake.street_address()
        started_at = gen_datetime()

        # случайное время поездки (от 5 до 120 минут)
        ride_time = random.randint(5, 120)

        #с шансом 2% поездка будет иметь статус отменена или еще в процессе
        ended_at = None if random.randint(1, 50) == 25 else gen_ride_end_time(started_at, ride_time)

        # цена = стоимость_подачи + (время_мин × тариф_за_мин)
        price = Decimal(str(100 + ride_time * (random.random() + 0.5)))

        #с шансом 15% пользователь оставит чаевые от 10 до 200 руб
        tip = Decimal("0.00") if random.randint(1, 100) > 15 else Decimal(str(random.randint(10, 200)) + ".00")


        fake_ride = Ride(
            id = ride_id,
            driver_id = driver_id,
            rider_id = user_id,
            starting_point = starting_point,
            destination = destination,
            started_at = started_at,
            ended_at = ended_at,
            ride_time =ride_time,
            price = price,
            tip = tip
        )

        return fake_ride

    def generate_user(self) -> User:
        """Сгенерировать объект пользователя"""
        user_id = str(random.randint(1_000_000_000_000_000, 10_000_000_000_000_000 - 1))
        username = self.fake.user_name()
        register_date = gen_datetime()

        user = User(
            id = user_id,
            username = username,
            register_date = register_date
        )
        return user

    def generate_driver(self) -> Driver:
        """Сгенерировать объект водителя"""

        user_id = str(random.randint(1_000_000_000_000_000, 10_000_000_000_000_000 - 1))
        username = self.fake.user_name()
        license_plate = self.fake.license_plate()
        register_date = gen_datetime()

        driver = Driver(
            id = user_id,
            username = username,
            license_plate = license_plate,
            register_date = register_date
        )

        return driver


