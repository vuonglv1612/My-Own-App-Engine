from attrs import asdict
from fastapi import APIRouter, Depends

from src.api.auth import current_user
from src.api.dependencies import unit_of_work
from src.core.entities import User
from src.services.unit_of_work import UnitOfWork

router = APIRouter()


@router.get("")
async def get_all_units(uow: UnitOfWork = Depends(unit_of_work), user: User = Depends(current_user)):
    async with uow:
        units = await uow.units.get_all()
        return {
            "units": [asdict(unit) for unit in units]
        }
