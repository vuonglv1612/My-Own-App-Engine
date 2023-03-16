import environs

env = environs.Env()
env.read_env()


class Settings:
    registry = env.str("REGISTRY")
    registry_namespace = env.str("REGISTRY_NAMESPACE")
    registry_username = env.str("REGISTRY_USERNAME")
    registry_password = env.str("REGISTRY_PASSWORD")
    file_path = env.str("FILE_PATH", '/tmp')
    build_folder = env.str("BUILD_FOLDER", '/tmp')
    builder = env.str("BUILDER", 'heroku/buildpacks:20')
    celery_broker_url = env.str("CELERY_BROKER_URL", "redis://localhost:6379")
    redis_url = env.str("REDIS_URL", "redis://localhost:6379")
    loki_url = env.str("LOKI_URL", "http://localhost/loki/api/v1/push")
    tsuru_api = env.str("TSURU_API", "http://tsuru:8080")
    tsuru_username = env.str("TSURU_USERNAME")
    tsuru_password = env.str("TSURU_PASSWORD")


settings = Settings()
