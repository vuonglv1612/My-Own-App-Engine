from datetime import datetime, timezone

from src.core.services import app as app_service


def test_create_app():
    project_id = "project_id"
    app_name = "test_app"
    created_at = datetime.now(tz=timezone.utc)
    app = app_service.create_app(project_id, app_name, created_at)

    assert app.project_id == project_id
    assert app.name == app_name
    assert app.status == "created"
    assert app.created_at == created_at
    assert app.deleted_at is None
