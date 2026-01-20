from infrastructure.data_generator_impl import FakeDataGenerator
from infrastructure.data_writer import DBWriter
import random
from time import sleep

def main():
    db_writer = DBWriter(
        host="localhost",
        port=5432,
        database="taxi"
    )

    try:

        data_generator = FakeDataGenerator()

        for _ in range(100):
            # генерация и запись пользователей в бд
            users = [data_generator.generate_user() for _ in range(random.randint(3, 10))]

            db_writer.create_user_batch(users)

            # генерация и запись водителей в бд
            drivers = [data_generator.generate_driver() for _ in range(random.randint(1, 4))]
            db_writer.create_driver_batch(drivers)

            # генерация и запись N (10-40) поездок в бд
            rides = []
            for _ in range(random.randint(40, 200)):
                random_user = random.choice(users)
                random_driver = random.choice(drivers)

                ride = data_generator.generate_ride(random_user.id, random_driver.id)
                rides.append(ride)
            db_writer.create_ride_batch(rides)

            sleep(1)

    except Exception as e:
        print(f"Ошибка {e}")

    finally:
        db_writer.close()

if __name__ == "__main__":
    main()