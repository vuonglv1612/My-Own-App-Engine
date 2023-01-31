import environs

env = environs.Env()
env.read_env()


class Settings:
    registry = env.str("REGISTRY")
    namespace = env.str("NAMESPACE")
    username = env.str("USERNAME")
    password = env.str("PASSWORD")
    file_path = env.str("FILE_PATH", '/tmp')
    build_folder = env.str("BUILD_FOLDER", '/tmp')
    builder = env.str("BUILDER", 'heroku/buildpacks:20')


settings = Settings()
