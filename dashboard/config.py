from environs import Env

env = Env()
env.read_env()  # read .env file, if it exists


class Settings:
    postgresql_uri = env("POSTGRESQL_URI")
    async_postgresql_uri = env("ASYNC_POSTGRESQL_URI")


settings = Settings()
