import os

from dotenv import load_dotenv

load_dotenv('.env')
APP_ENV = os.getenv("APP_ENV", "local")
print(f"INFO:     Loading configuration for environment: {APP_ENV}")
# Tạo đường dẫn tới file .env tương ứng
env_file_path = f".env.{APP_ENV}"
print(f"INFO:     Using environment file: {env_file_path}")
