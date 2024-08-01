from fastapi import FastAPI

from files.routes import router as files_router

app = FastAPI(
    title="files"
)

app.include_router(
    files_router
)
