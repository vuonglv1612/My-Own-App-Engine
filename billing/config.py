import environs

env = environs.Env()
env.read_env()


class Settings:
    postgresql_uri = env.str("POSTGRESQL_URI")


settings = Settings()
