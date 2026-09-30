import datetime
import random
import string
from faker import Faker


fake = Faker()

class DataGenerator:

    @staticmethod
    def generate_random_email():
        return fake.email()

    @staticmethod
    def generate_random_password():
        random_string = ''.join(
            random.choices(
                string.ascii_letters + string.digits,
                k=10
            )
        )
        return f"Test_{random_string}1@"

    @staticmethod
    def generate_random_name():
        names = [
            "Иван",
            "Алексей",
            "Максим",
            "Дмитрий",
            "Андрей",
            "Сергей",
            "Михаил"
        ]
        surnames = [
            "Иванов",
            "Петров",
            "Сидоров",
            "Смирнов",
            "Кузнецов",
            "Попов",
            "Васильев"
        ]

        return f"{random.choice(names)} {random.choice(surnames)}"

    @staticmethod
    def generate_random_movie():
        return {
            "name": f"Тестовый фильм {fake.uuid4()[:8]}",
            "imageUrl": fake.image_url(),
            "price": fake.random_int(min=100, max=1000),
            "description": fake.sentence(nb_words=10),
            "location": "MSK",
            "published": True,
            "genreId": 8,
        }



    @staticmethod
    def generate_user_data() -> dict:
        """Генерирует данные для тестового пользователя"""
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',  # генерируем UUID как строку
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }