from typing import Optional, Union, Dict

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager, IntegerIDMixin, schemas, models, exceptions

from src.services import get_object_by_username
from src.database import get_user_db
from src.validators import validate_username, validate_email, auth_form_exception, check_passwords
from .models import User
from .schemas import UserPasswordChange


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):

    async def validate_password(self, password: str, user: Union[schemas.UC, models.UP]) -> None:
        if len(password) < 6:
            raise auth_form_exception(
                'password', 'password should be at least 6 characters'
            )
        return

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:

        await self.validate_password(user_create.password, user_create)

        await validate_username(user_create.username)

        existing_user = await self.user_db.get_by_email(user_create.email)
        await validate_email(existing_user)

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def authenticate(
        self,
        credentials: OAuth2PasswordRequestForm,
    ) -> Optional[models.UP]:
        try:
            user = await self.get_by_email(credentials.username)
        except exceptions.UserNotExists:
            user = await get_object_by_username(User, credentials.username)
            if user is None:
                self.password_helper.hash(credentials.password)
                return
        if user:
            verified, updated_password_hash = self.password_helper.verify_and_update(
                credentials.password, user.hashed_password
            )
            if not verified:
                return
            if updated_password_hash is not None:
                await self.user_db.update(user, {"hashed_password": updated_password_hash})

            return user

    async def check_password(self, data: UserPasswordChange, user: User) -> Dict[str, str]:
        is_math_old_password, _ = self.password_helper.verify_and_update(
            data.old_password, user.hashed_password
        )
        await check_passwords(
            is_math_old_password, data.new_password, data.new_password_confirm
        )
        await self.validate_password(data.new_password, user)

        new_hashed_password = self.password_helper.hash(data.new_password)
        await self.user_db.update(user, {'hashed_password': new_hashed_password})

        return {'success': 'password changed'}


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
