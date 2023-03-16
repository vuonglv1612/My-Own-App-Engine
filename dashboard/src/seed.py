from .core.entities import Unit
from .dependencies import create_session_factory

session_factory = create_session_factory()


async def units_seeding():
    session = session_factory()
    units = [
        Unit(id="c100_m100", cpu=100, memory=100, active=True,
             plan_name="c0.1m0.2"),
        Unit(id="c200_m200", cpu=200, memory=200, active=True,
             plan_name="c0.1m0.2"),
        Unit(id="c300_m300", cpu=300, memory=300, active=True,
             plan_name="c0.1m0.2"),
    ]
    for unit in units:
        session.add(unit)
    await session.commit()
