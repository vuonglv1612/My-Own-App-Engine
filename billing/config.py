import environs

env = environs.Env()
env.read_env()


class Settings:
    postgresql_uri = env.str("POSTGRESQL_URI")
    async_postgresql_uri = env.str("ASYNC_POSTGRESQL_URI")


settings = Settings()
