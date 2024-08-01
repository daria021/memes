import os

from fastapi import BackgroundTasks, Depends, HTTPException, APIRouter
from fastapi import UploadFile, File
from fastapi.responses import FileResponse

from dependencies.services import get_memes_service
from meme.schemas import MemeCreate
from services.MemesService import MemesService
from services.exceptions import WrongKeyException, ServerNotAvailableException
from .exceptions import NotFoundException

router = APIRouter(
    prefix="/meme",
    tags=["Memes"]
)


@router.post("")
async def upload_meme(
        create_schema: MemeCreate = Depends(MemeCreate),
        image: UploadFile = File(...),
        memes_service: MemesService = Depends(get_memes_service)
):
    try:
        meme = await memes_service.upload_meme(image=image, meme=create_schema)
    except ServerNotAvailableException:
        raise HTTPException(status_code=500, detail="Something went wrong, please ty again later")

    return meme


@router.delete("/{key}")
async def delete_meme(
        key: str,
        memes_service: MemesService = Depends(get_memes_service)
):
    try:
        await memes_service.delete_meme(key=key)
    except (NotFoundException, WrongKeyException):
        raise HTTPException(status_code=404, detail=f"Meme with id {key} not found")
    except ServerNotAvailableException:
        raise HTTPException(status_code=500, detail="Something went wrong, please ty again later")


@router.get("/{key}/image")
async def get_meme_image(
        key: str,
        background_tasks: BackgroundTasks,
        memes_service: MemesService = Depends(get_memes_service),
):
    try:
        filepath, filename = await memes_service.get_meme_image(key=key)
    except WrongKeyException:
        raise HTTPException(status_code=404, detail=f"Meme with id {key} not found")
    except ServerNotAvailableException:
        raise HTTPException(status_code=500, detail="Something went wrong, please try again later")

    background_tasks.add_task(os.remove, filepath)

    return FileResponse(path=filepath, filename=filename, media_type="image/jpeg")


@router.get("/{key}")
async def get_meme_info(
        key: str,
        memes_service: MemesService = Depends(get_memes_service),
):
    try:
        meme = await memes_service.get_meme_info(key=key)
    except NotFoundException:
        raise HTTPException(status_code=404, detail=f"Meme with id {key} not found")

    return meme
