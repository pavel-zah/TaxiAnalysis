from domain.services.data_generator import DataGenerator
from domain.entities.ride import Ride
from domain.entities.user import User
from domain.entities.driver import Driver
from datetime import datetime, timedelta
import random
from faker import Faker
from decimal import Decimal, getcontext

getcontext().prec = 2

def gen_date_skewed(min_year=2020, max_year=datetime.now().year):
    start = datetime(min_year, 1, 1)
    end = datetime(max_year, 12, 31, 23, 59, 59)

    r = random.random() ** 0.25  # сильный перекос к концу
    return start + (end - start) * r


def gen_hour_realistic(dt: datetime):
    weekday = dt.weekday()  # 0=пн ... 6=вс
    is_weekend = weekday >= 5
    is_friday = weekday == 4

    intervals = [
        ((0, 5), 0.03),    # ночь
        ((6, 7), 0.07),    # раннее утро
        ((8, 10), 0.28),   # утренний пик
        ((11, 16), 0.20),  # дневное время
        ((17, 19), 0.30),  # вечерний пик
        ((20, 23), 0.12),  # поздний вечер
    ]

    # выходные — меньше утром, больше вечером
    if is_weekend:
        intervals = [
            ((0, 6), 0.05),
            ((7, 10), 0.10),
            ((11, 16), 0.25),
            ((17, 22), 0.45),
            ((23, 23), 0.15),
        ]

    # пятничный вечер — отдельный буст
    if is_friday:
        intervals.append(((20, 22), 0.20))

    ranges, weights = zip(*intervals)
    chosen = random.choices(ranges, weights=weights)[0]

    return random.randint(chosen[0], chosen[1])


def gen_datetime(min_year=2020, max_year=datetime.now().year) -> datetime:
    dt = gen_date_skewed(min_year, max_year)

    hour = gen_hour_realistic(dt)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    return dt.replace(hour=hour, minute=minute, second=second)

def gen_ride_time():
    # пик ~15–25 минут, длинные поездки редкие
    base = int(random.lognormvariate(2.7, 0.6))
    return max(5, min(base, 120))

def gen_end_time(started_at, ride_time):
    hour = started_at.hour

    cancel_prob = 0.01
    if hour < 6:
        cancel_prob = 0.04
    elif hour in (8, 9, 18, 19):
        cancel_prob = 0.02

    if random.random() < cancel_prob:
        return None

    return started_at + timedelta(minutes=ride_time)

def gen_price(ride_time):
    base_fee = random.choice([99, 129, 149])
    per_minute = random.uniform(12, 20)

    # длинные поездки — дешевле за минуту
    if ride_time > 40:
        per_minute *= 0.85

    price = base_fee + ride_time * per_minute
    return Decimal(price).quantize(Decimal("1.00"))


def gen_tip(started_at, price):
    weekday = started_at.weekday()
    is_weekend = weekday >= 5
    hour = started_at.hour

    prob = 0.12
    if is_weekend:
        prob += 0.08
    if hour >= 18:
        prob += 0.05

    if random.random() > prob:
        return Decimal("0.00")

    tips = [50, 100, 150, 200, 300]
    tip = random.choice(tips)

    # иногда процент от цены
    if random.random() < 0.3:
        tip = int(price * random.choice([0.05, 0.1]))

    return Decimal(tip).quantize(Decimal("1.00"))

def gen_addresses(fake):
    if random.random() < 0.6:
        street = fake.street_name()
        return street + " 10", street + " 55"
    return fake.street_address(), fake.street_address()



def gen_ride_end_time(ride_start: datetime, duration_minutes) -> datetime:
    """ создает datetime - время конца поездки """
    ride_duration = timedelta(minutes=duration_minutes)
    return ride_start + ride_duration


class FakeDataGenerator(DataGenerator):
    """Класс для создания фейковых данных"""

    def __init__(self, model_name="qwen/qwen3-vl-4b"):
        self.fake = Faker("ru_RU")

    def generate_ride(self, user_id, driver_id) -> Ride:
        ride_id = str(random.randint(10 ** 15, 10 ** 16 - 1))

        starting_point, destination = gen_addresses(self.fake)

        started_at = gen_datetime()
        ride_time = gen_ride_time()
        ended_at = gen_end_time(started_at, ride_time)

        price = gen_price(ride_time)
        tip = gen_tip(started_at, price)

        return Ride(
            id=ride_id,
            driver_id=driver_id,
            rider_id=user_id,
            starting_point=starting_point,
            destination=destination,
            started_at=started_at,
            ended_at=ended_at,
            price=price,
            tip=tip
        )

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


