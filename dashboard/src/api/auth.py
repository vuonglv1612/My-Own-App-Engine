from fastapi import HTTPException, status, Depends

from src.core.models import Project


def current_project():
    # TODO: get current project from request context
    return Project(id="project_id", name="project_name")


def user_permissions():
    # TODO: get user permissions from request context
    return ["test_cases:read", "test_cases:write"]


def check_required_permissions(required_permissions):
    def inner_depends(permissions=Depends(user_permissions)):
        missing_permissions = set(required_permissions) - set(permissions)
        if missing_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": "You don't have required permissions({})".format(", ".join(missing_permissions))},
            )

    return inner_depends
