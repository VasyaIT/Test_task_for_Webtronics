from typing import Callable

from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST

from src.base import Base
from .models import Post, Like, DisLike
from src.services import get_object_by_id, do_rate
from src.users.models import User


async def get_post_or_404_not_owner(pk: int, user: User) -> None | HTTPException:
    post = await get_object_by_id(Post, pk)
    if not post:
        raise HTTPException(HTTP_404_NOT_FOUND)
    if post.id in [p.id for p in user.posts]:
        raise HTTPException(HTTP_403_FORBIDDEN, "You can't rate own posts")


async def post_rate(
        pk: int, action: str, user: User
) -> Callable[[Base, Base, int, int], None | Exception]:
    user_id = user.id
    if action == 'like':
        await do_rate(Like, DisLike, pk, user_id)
    elif action == 'dislike':
        await do_rate(DisLike, Like, pk, user_id)
    else:
        raise HTTPException(HTTP_400_BAD_REQUEST)
