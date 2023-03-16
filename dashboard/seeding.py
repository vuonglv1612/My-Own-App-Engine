import asyncio

from src.dependencies import start_mappers
from src.seed import units_seeding


async def main():
    await units_seeding()


if __name__ == "__main__":
    start_mappers()
    asyncio.run(main())
