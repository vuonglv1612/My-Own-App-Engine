from attrs import asdict
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer

from .auth0 import VerifyToken, get_user_info
from .dependencies import unit_of_work, get_billing_client, get_redis_client
from ..core.entities import User
from ..core.services.create_user import CreateUserCommand, CreateUserUserCase
from ..services.billing import BillingClient
from ..services.unit_of_work import UnitOfWork


async def verify_token(token=Depends(HTTPBearer())):
    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": result.get("message")},
        )
    return token.credentials, result


async def current_user(credential=Depends(verify_token), uow: UnitOfWork = Depends(unit_of_work),
                       billing_client: BillingClient = Depends(get_billing_client),
                       redis_client=Depends(get_redis_client)):
    token, user_payload = credential
    sub = user_payload.get("sub")
    userinfo = await get_user_info(redis_client, sub, token)
    if not userinfo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid token"},
        )
    email = userinfo.get("email")
    name = userinfo.get("name")
    if not name:
        name = email
    sub = userinfo.get("sub")
    # find user in db
    async with uow:
        user = await uow.users.get_by_id(sub)
        if user:
            data = asdict(user)
            return User(**data)
    async with uow:
        command = CreateUserCommand(email=email, name=name, sub=sub)
        handler = CreateUserUserCase(uow, billing_client)
        try:
            user = await handler.execute(command)
        except Exception as e:
            print("Error when create user: ", e)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": f"User {email} not found"},
            )
        else:
            data = asdict(user)
            return User(**data)
