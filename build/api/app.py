import asyncio
import os
import shutil
from functools import partial

import aiofiles
from fastapi import FastAPI, File, UploadFile, Body
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from config import settings
from use_cases.build_from_zip import build_from_zip
from functions import push

app = FastAPI()


async def run_in_thread(func):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func)


class BuildFromZipRequest(BaseModel):
    image_name: str
    image_tag: str
    buildpack: str = None


@app.post("/build-from-zip")
async def build_from_zip_router(
    user_id: str = Body(...),
    image_name: str = Body(...),
    version: str = Body(..., example="v1.0"),
    buildpack: str = Body(None),
    file: UploadFile = File(...),
):
    # Save file to disk
    file_name = os.path.join(settings.file_path, user_id, file.filename)
    build_folder = os.path.join(
        settings.build_folder, user_id, file.filename.replace(".", "_")
    )
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    async with aiofiles.open(file_name, "wb") as buffer:
        await buffer.write(await file.read())

    async def _build_from_zip():
        async for data in await run_in_thread(
            partial(
                build_from_zip,
                file_name,
                build_folder,
                image_name,
                version,
                settings.builder,
                buildpack,
            )
        ):
            yield data
        async for data in await run_in_thread(
            partial(
                push,
                image_name,
                version,
                settings.registry,
                settings.namespace,
                settings.username,
                settings.password,
            )
        ):
            yield data

    return StreamingResponse(_build_from_zip(), media_type="text/plain")


@app.post("/build-from-git")
def build_from_git():
    pass
