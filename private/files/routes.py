from fastapi import APIRouter, UploadFile, Depends
from starlette.responses import FileResponse

from dependencies.repositories import get_files_service
from s3.service import FilesService

router = APIRouter(
    prefix="/files",
    tags=["Image", ]
)


@router.post("/{key}")
async def upload_file(
        key: str,
        file: UploadFile,
        files: FilesService = Depends(get_files_service),
):
    filepath = f"temp/{key}"
    with open(filepath, "wb") as tempfile:
        tempfile.write(await file.read())

    created_file = await files.upload_file(key=key)
    return created_file


@router.get("/{key}")
async def get_file(
        key: str,
        files: FilesService = Depends(get_files_service),
):
    created_filepath = await files.get_file(key=key)
    return FileResponse(path=created_filepath, filename=key, media_type="multipart/form-data")


@router.delete("/{key}")
async def delete_file(
        key: str,
        files: FilesService = Depends(get_files_service),
):
    deleted_file = await files.delete_file(key=key)
    return deleted_file
