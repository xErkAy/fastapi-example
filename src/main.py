from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import uvicorn
from fastapi import FastAPI
from tortoise import Tortoise

from apps.authentication.routes import router as auth_router
from apps.test.routes import router as test_router
from core.authentication.middlewares import AuthenticationMiddleware
from core.settings import DATABASE


@asynccontextmanager
async def lifespan(*args: Any, **kwargs: dict[str, Any]) -> AsyncGenerator[None, Any]:
    await Tortoise.init(DATABASE)
    await Tortoise.generate_schemas()

    yield
    await Tortoise.close_connections()


app = FastAPI(lifespan=lifespan)
app.include_router(router=auth_router)
app.include_router(router=test_router)
app.add_middleware(AuthenticationMiddleware)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
