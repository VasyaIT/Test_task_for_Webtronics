from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.posts.routers import posts_router
from src.users.routers import fastapi_users, user_router
from src.users.authentication import auth_backend
from src.users.schemas import UserCreate, UserReadUpdate
from .config import CORS_ORIGIN, ALLOW_METHODS, ALLOW_HEADERS


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGIN,
    allow_credentials=True,
    allow_methods=ALLOW_METHODS,
    allow_headers=ALLOW_HEADERS,
)

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(
    fastapi_users.get_register_router(UserReadUpdate, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(user_router)
app.include_router(posts_router)
