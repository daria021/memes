from fastapi import FastAPI

from meme.routes import router as meme_router

app = FastAPI(
    title="meme"
)

app.include_router(
    meme_router
)
