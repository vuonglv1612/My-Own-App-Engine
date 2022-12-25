from datetime import datetime

from ..models import App


def create_app(organization_id: str, app_name: str, created_at: datetime) -> App:
    app = App.create(organization_id, app_name, created_at)
    return app
