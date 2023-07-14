from sqlalchemy import BigInteger, String, ForeignKey, Text, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.base import Base


class Like(Base):
    __tablename__ = 'likes'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True)
    user_id = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'))
    post_id = mapped_column(BigInteger, ForeignKey('posts.id', ondelete='CASCADE'))


class DisLike(Base):
    __tablename__ = 'dislikes'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True)
    user_id = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'))
    post_id = mapped_column(BigInteger, ForeignKey('posts.id', ondelete='CASCADE'))


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    user_id = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'))

    author = relationship('User', back_populates='posts', lazy='selectin')
    user_liked = relationship(Like, backref='post', lazy='selectin')
    user_disliked = relationship(DisLike, backref='post', lazy='selectin')
