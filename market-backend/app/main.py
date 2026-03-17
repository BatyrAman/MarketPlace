from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from sqlmodel import SQLModel

from app.core.config import settings
from app.core.exceptions import AppException, app_exception_handler
from app.db.session import engine

from app.routers.auth import router as auth_router
from app.routers.category import router as category_router
from app.routers.product import router as product_router
from app.routers.cart import router as cart_router
from app.routers.order import router as order_router
from app.routers.review import router as review_router
from app.routers.user import router as user_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(AppException, app_exception_handler)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={'detail': exc.errors()},
    )


@app.get('/')
async def healthcheck():
    return {'message': 'Marketplace API is running'}


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(review_router)
