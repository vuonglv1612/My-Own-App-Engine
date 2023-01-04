from datetime import datetime

from src.core.entities import App, Project, Plan


def create_app(project: Project, plan: Plan, app_name: str, created_at: datetime) -> App:
    app = App.create(project_id=project.id, plan_id=plan.id, app_name=app_name, created_at=created_at)
    return app
