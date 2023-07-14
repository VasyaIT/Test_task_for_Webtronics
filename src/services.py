from typing import Callable, Dict, Any, Union, List

from fastapi import HTTPException
from sqlalchemy import select, Select, update, Update, insert, Insert, delete, Delete
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_400_BAD_REQUEST

from src.posts.models import Post
from .database import async_session_maker
from src.users.models import User
from .base import Base


GET_MODEL = Callable[[Select, bool], Base | List[Base] | None | Any]
UPDATE_MODEL = Callable[[Update | Insert | Delete], None]


async def get_objects(obj: Base) -> GET_MODEL:
    return await get_model_or_none(select(obj), False)


async def get_object_by_id(obj: Base, obj_id: int) -> GET_MODEL:
    query = select(obj).where(obj.id == int(obj_id))
    return await get_model_or_none(query, True)


async def get_object_by_username(obj: Base, username: str) -> GET_MODEL:
    query = select(obj).where(obj.username == username)
    return await get_model_or_none(query, True)


async def update_user(user_id: int, data: Dict[str, Any]) -> UPDATE_MODEL:
    stmt = update(User).values(data).where(User.id == user_id)
    return await update_insert_delete_model_or_none(stmt)


async def get_post_by_user_id(pk: int, user_id: int) -> GET_MODEL:
    query = select(Post).where(Post.id == pk, Post.user_id == user_id)
    return await get_model_or_none(query, True)


async def update_insert_post(is_update: bool, data: Dict[str, Any]) -> UPDATE_MODEL:
    if is_update:
        stmt = update(Post).values(data)
    else:
        stmt = insert(Post).values(data)
    return await update_insert_delete_model_or_none(stmt)


async def post_delete(post_id: int) -> UPDATE_MODEL:
    stmt = delete(Post).where(Post.id == post_id)
    return await update_insert_delete_model_or_none(stmt)


async def get_model_or_none(query: Select, one: bool) -> Union[Base, List[Base], None, Any]:
    async with async_session_maker() as session:
        result = await session.execute(query)
    try:
        if one:
            model = result.scalar()
        else:
            model = result.scalars().all()
    except ValueError:
        return
    return model


async def update_insert_delete_model_or_none(statement: Update | Insert | Delete) -> None:
    async with async_session_maker() as session:
        try:
            await session.execute(statement)
        except IntegrityError:
            raise HTTPException(HTTP_400_BAD_REQUEST, 'Error, try again')
        await session.commit()


async def do_rate(obj: Base, del_obj: Base, pk: int, user_id: int) -> None | Exception:
    async with async_session_maker() as session:
        query = select(obj).where(obj.user_id == user_id, obj.post_id == pk)
        result = await session.execute(query)

        if result.scalar():
            await session.execute(delete(obj).where(obj.user_id == user_id, obj.post_id == pk))
        else:
            session.add(obj(user_id=user_id, post_id=pk))
            await session.execute(
                delete(del_obj).where(del_obj.user_id == user_id, del_obj.post_id == pk)
            )

        try:
            await session.commit()
        except Exception:
            await session.rollback()
            raise
