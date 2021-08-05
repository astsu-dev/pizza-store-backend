import uvicorn
from fastapi import FastAPI

from pizza_store.db.db import init_models
from pizza_store.routers import router
from pizza_store.settings import settings

app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def on_start() -> None:
    await init_models()


if __name__ == "__main__":
    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
