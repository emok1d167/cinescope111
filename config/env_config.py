import os

from dotenv import load_dotenv


load_dotenv()


class EnvConfig:

    @staticmethod
    def get(name: str, default=None):
        return os.getenv(name, default)

    @staticmethod
    def require(name: str) -> str:
        value = os.getenv(name)

        if not value:
            raise ValueError(f"Environment variable '{name}' is not set")

        return value