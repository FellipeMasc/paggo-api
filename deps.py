import asyncio
from prisma import Prisma
from collections.abc import Generator
from typing import Annotated
from typing import AsyncGenerator
from fastapi import Depends

async def get_db() -> AsyncGenerator[Prisma, None]:
    db = Prisma()
    await db.connect()
    try :
        yield db
    finally:
        await db.disconnect()