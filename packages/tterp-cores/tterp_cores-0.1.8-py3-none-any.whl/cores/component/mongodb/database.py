from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection
from pymongo.database import Database

from cores.config import service_config

# Thông số kết nối MongoDB
MONGO_URI = (
    f"mongodb://{service_config.MONGODB_USERNAME}:{service_config.MONGODB_PASSWORD}@"
    f"{service_config.MONGODB_HOST}:{service_config.MONGODB_PORT}/"
    f"{service_config.MONGODB_DATABASE}?authSource="
    f"{service_config.MONGODB_AUTHENTICATION_DATABASE}"
)
if service_config.APP_ENV == "local":
    MONGO_URI = (
        f"mongodb://{service_config.MONGODB_HOST}:{service_config.MONGODB_PORT}/"
        f"{service_config.MONGODB_DATABASE}"
    )
DATABASE_NAME = service_config.MONGODB_DATABASE


def get_mongo_uri() -> str:
    return MONGO_URI  # hoặc lấy từ config


def get_mongo_database_name() -> str:
    return DATABASE_NAME


# # Khởi tạo client và database
# client: Optional[AsyncIOMotorClient] = None
# db: Optional[Database] = None


def get_mongodb():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DATABASE_NAME]
    return db


def get_test_mongodb():
    uri = (
        f"mongodb://{service_config.MONGODB_HOST}:{service_config.MONGODB_PORT}/"
        f"test_{service_config.MONGODB_DATABASE}"
    )
    client = AsyncIOMotorClient(uri)
    db = client[f"test_{service_config.MONGODB_DATABASE}"]
    return db


def get_collection(
    db: Database,
    collection_name: str,
) -> Collection:
    """Lấy một collection từ database."""
    return db[collection_name]
