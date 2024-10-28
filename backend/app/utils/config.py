import os
from dotenv import load_dotenv

environment = os.getenv(
    "ENVIRONMENT", "development"
)  # production or development

if environment == "development":
    load_dotenv(".env.local")


def get_env(key: str, default: str = None) -> str:
    return os.getenv(key, default)
