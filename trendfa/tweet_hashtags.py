# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta

from trendfa.database import session
from trendfa.models import Word, Tweet
from sqlalchemy import desc
from sqlalchemy import func

from trendfa.twitter import api as twitter_api

TIME_RANGE = timedelta(days=1)


def get_hashtag_trends(time_range, limit=3):
    return session.query(Word.word, func.count(Word.id))\
        .filter(Word.time >= (datetime.now() - time_range))\
        .filter(func.substr(Word.word, 1, 1) == '#')\
        .group_by(Word.word)\
        .order_by(desc(func.count(Word.id)))\
        .limit(limit).all()


def get_trends_tweet():
    return 'هشتگ‌های پر‌طرفدار:\n\n{trends}'.format(
        trends='\n'.join(
            '- {word}'.format(word=word.encode('latin1').decode('utf-8')) for word, count in get_hashtag_trends(TIME_RANGE)
        )
    )


if __name__ == '__main__':
    import sys

    trends = get_trends_tweet()

    print (trends)

    if len(sys.argv) > 1 and sys.argv[1] == '--send' and trends is not None:
        twitter_api.update_status(trends)
        print ('Sent')

