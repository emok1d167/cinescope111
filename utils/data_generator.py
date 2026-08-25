import random
import string


class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string = ''.join(
            random.choices(
                string.ascii_lowercase + string.digits,
                k=10
            )
        )
        return f"test_{random_string}@mail.com"

    @staticmethod
    def generate_random_password():
        random_string = ''.join(
            random.choices(
                string.ascii_letters + string.digits,
                k=10
            )
        )
        return f"Test_{random_string}1!"

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