from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from bottles.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    nick = Column(String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User: {} {}>'.format(self.id, self.nick)

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    created = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    title = Column(String(80), nullable=False)
    body = Column(String(80), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'))

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    subscriber_id = Column(Integer, ForeignKey('users.id'))
    target_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return (
            '<Subscription: {} to {}>'
            .format(self.subscriber_id, self.target_id)
        )