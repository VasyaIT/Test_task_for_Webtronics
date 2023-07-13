from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers
from starlette import status

from src.services import get_objects, update_user, get_object_by_username
from .authentication import auth_backend
from .manager import get_user_manager
from .models import User
from .schemas import UserReadUpdate

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

get_user_or_401 = fastapi_users.current_user()
get_user_or_none = fastapi_users.current_user(optional=True)
is_superuser_or_403 = fastapi_users.current_user(superuser=True)

auth_router = APIRouter(prefix='/auth', tags=['auth'])
user_router = APIRouter(prefix='/account', tags=['users'])


@user_router.get('/me', name='user:me', response_model=UserReadUpdate)
async def user_me(user: User = Depends(get_user_or_401)):
    return user


@user_router.patch('/me/update', name='user:update')
async def user_me_update(data: UserReadUpdate, user: User = Depends(get_user_or_401)):
    await update_user(user.id, data.dict())
    return {'success': 'account updated successfully'}


@user_router.get(
    '/users', name='user:users',
    dependencies=[Depends(is_superuser_or_403)],
    response_model=List[UserReadUpdate]
)
async def user_list():
    return await get_objects(User)


@user_router.get('/user/{username}', name='user:user', response_model=UserReadUpdate)
async def user_account(username: str):
    user = await get_object_by_username(User, username)

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return user
