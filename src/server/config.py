import os
from loguru import logger
from peewee import PostgresqlDatabase, SqliteDatabase

env_config = {
    "username": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
    "host": os.environ.get("POSTGRES_HOST"),
    "database": os.environ.get("POSTGRES_DB"),
    "port": os.environ.get("POSTGRES_PORT"),
}

allowed_origins = os.environ.get("ALLOWED_ORIGINS", "*").split(",")
allow_credentials = os.environ.get("ALLOW_CREDENTIALS", True)
allow_methods = os.environ.get("ALLOW_METHODS", "*").split(",")
allow_headers = os.environ.get("ALLOW_HEADERS", "*").split(",")
generator_url = os.environ.get("GENERATOR_URL", "http://localhost:8010")
testing = os.environ.get("TESTING", False)


def is_config_empty(config: dict):
    for key, value in config.items():
        if not value:
            return True
    return False


def get_db_engine():
    if testing:
        logger.debug("Creating in-memory database for testing")
        return SqliteDatabase(":memory:", pragmas={"foreign_keys": 1})

    if not is_config_empty(env_config):
        logger.debug("Postgres connection found")
        return PostgresqlDatabase(
            database=env_config["database"],
            host=env_config["host"],
            user=env_config["username"],
            password=env_config["password"],
            port=env_config["port"],
        )
    logger.critical("Error in DB configuration")
