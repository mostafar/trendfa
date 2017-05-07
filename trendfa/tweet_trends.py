# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta

from trendfa.database import session
from trendfa.models import Word
from sqlalchemy import desc
from sqlalchemy import func

from trendfa.twitter import api as twitter_api


def get_trends(time_range, limit=7):
    return session.query(Word.word, func.count(Word.id))\
        .filter(Word.time >= (datetime.now() - time_range))\
        .group_by(Word.word)\
        .order_by(desc(func.count(Word.id)))\
        .limit(limit).all()


def get_trends_tweet():
    text = 'ترند در ۲۴ ساعت گذشته:\n'

    for word, count in get_trends(timedelta(days=1)):
        text += '- {}\n'.format(word.encode('latin1').decode('utf-8'))

    return text


if __name__ == '__main__':
    import sys

    trends = get_trends_tweet()

    print (trends)

    if len(sys.argv) > 1 and sys.argv[1] == '--send':
        twitter_api.update_status(trends)
        print ('Sent')
