from datetime import datetime

from src.core.models import App


def create_app(project_id: str, plan_name: str, app_name: str, created_at: datetime) -> App:
    app = App.create(project_id, plan_name, app_name, created_at)
    return app
