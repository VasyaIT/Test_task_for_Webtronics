from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

from src.users.models import User
from src.users.routers import get_user_or_401
from src import services
from .utils import get_post_or_404_not_owner, post_rate
from .models import Post
from .schemas import PostRead, PostCreateUpdate, BasePost

posts_router = APIRouter(prefix='/posts', tags=['posts'])


@posts_router.get('/', response_model=List[BasePost])
async def all_post():
    post_list = await services.get_objects(Post)
    return post_list if post_list else []


@posts_router.get('/post/{pk}', response_model=PostRead, dependencies=[Depends(get_user_or_401)])
async def read_post(pk: int):
    post = await services.get_object_by_id(Post, pk)
    if not post:
        raise HTTPException(HTTP_404_NOT_FOUND)
    return post


@posts_router.post('/create/')
async def create_post(
        data: PostCreateUpdate, user: User = Depends(get_user_or_401)
) -> Dict[str, str]:
    form = data.dict()
    form['user_id'] = user.id
    await services.update_insert_post(False, form)  # exception is handled internally
    return {'success': 'post added'}


@posts_router.patch('/update/{pk}')
async def update_post(
        pk: int, data: PostCreateUpdate, user: User = Depends(get_user_or_401)
) -> Dict[str, str]:
    if pk not in [post.id for post in user.posts]:
        raise HTTPException(HTTP_403_FORBIDDEN)
    form = data.dict()
    form['user_id'] = user.id
    await services.update_insert_post(True, form)  # exception is handled internally
    return {'success': 'post updated'}


@posts_router.delete('/delete/{pk}')
async def delete_post(pk: int, user: User = Depends(get_user_or_401)) -> Dict[str, str]:
    if pk not in [post.id for post in user.posts]:
        raise HTTPException(HTTP_403_FORBIDDEN)
    await services.post_delete(pk)  # exception is handled internally
    return {'success': 'post deleted'}


@posts_router.post('/action/{pk}')
async def rate_post(pk: int, action: str, user: User = Depends(get_user_or_401)):
    await get_post_or_404_not_owner(pk, user)
    await post_rate(pk, action, user)
    return {'success': 'post is rated'}
