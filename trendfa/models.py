from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Tweet(Base):
    __tablename__ = 'tweet'

    id = Column(Integer, primary_key=True, autoincrement=True)
    twitter_id = Column(Text, unique=True)
    text = Column(Text)
    time = Column(DateTime)
    likes = Column(Integer)
    retweets = Column(Integer)

    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship('Author')


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True, autoincrement=True)
    twitter_id = Column(Text, unique=True)
    screen_name = Column(Text)
    followers_count = Column(Integer)

