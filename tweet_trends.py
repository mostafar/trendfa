# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta

from sqlalchemy import desc
from sqlalchemy import func

from database import session
from models import Word
from twitter import api as twitter_api


def get_trends(time_range, limit=5):
    return session.query(Word.word, func.count(Word.id))\
        .filter(Word.time >= (datetime.now() - time_range))\
        .group_by(Word.word)\
        .order_by(desc(func.count(Word.id)))\
        .limit(limit).all()


def get_trends_tweet():
    text = 'ترند در ۴۸ ساعت گذشته:\n'

    for word, count in get_trends(timedelta(days=2)):
        text += '- {}\n'.format(word.encode('latin1').decode('utf-8'))

    return text


if __name__ == '__main__':
    twitter_api.update_status(get_trends_tweet())
