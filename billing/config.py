import environs

env = environs.Env()
env.read_env()


class Settings:
    postgresql_uri = env.str("POSTGRESQL_URI")
    async_postgresql_uri = env.str("ASYNC_POSTGRESQL_URI")
    overdue_invoice_schedule_interval = env.int("OVERDUE_INVOICE_SCHEDULE_INTERVAL")
    renew_interval = env.int("RENEW_INTERVAL")

settings = Settings()
