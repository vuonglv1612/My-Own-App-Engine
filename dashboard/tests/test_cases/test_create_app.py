from datetime import datetime, timezone

import pytest

from src.handlers import app as app_handlers
from src.utils.datetime import model_to_dict


@pytest.mark.asyncio
async def test_create_app(uow_factory, provisioner_factory):
    project_id = "project_id"
    app_name = "test-app"
    plan = "c0.1m256"
    created_at = datetime.now(tz=timezone.utc)
    uow = uow_factory.for_test_create_app()
    provisioner = provisioner_factory.for_test_create_app()

    app = await app_handlers.new_app(uow, provisioner, project_id, plan, app_name, created_at)

    persisted_app = await uow.apps.get_by_id(app_name)
    assert uow.committed
    assert persisted_app is not None
    assert model_to_dict(persisted_app) == app
    assert provisioner.get_app(app_name) is not None
