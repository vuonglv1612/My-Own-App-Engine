from dependencies import unit_of_work_factory


async def unit_of_work():
    return unit_of_work_factory()
