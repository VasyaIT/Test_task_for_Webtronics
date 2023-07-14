from pydantic import BaseModel, validator

from src.users.schemas import UserReadUpdate


class BasePost(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True


class PostRead(BasePost):
    user_liked: list
    user_disliked: list
    author: UserReadUpdate

    @validator('user_liked')
    def count_likes(cls, likes):
        return len(likes)

    @validator('user_disliked')
    def count_dislikes(cls, dislikes):
        return len(dislikes)


class PostCreateUpdate(BasePost):
    pass


class Action(BaseModel):
    like: str
    dislike: str

    class Config:
        orm_mode = True
