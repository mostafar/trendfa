# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta

from trendfa.database import session
from trendfa.models import Word, Tweet
from sqlalchemy import desc
from sqlalchemy import func

from trendfa.twitter import api as twitter_api

TIME_RANGE = timedelta(days=1)
LATIN_TO_PERSIAN = {latin: persian for latin, persian in [('0', '۰'), ('1', '۱'), ('2', '۲'), ('3', '۳'), ('4', '۴'), ('5', '۵'), ('6', '۶'), ('7', '۷'), ('8', '۸'), ('9', '۹'),]}

def persian_number(number):
    number = str(number)
    return ''.join([LATIN_TO_PERSIAN[c] if c in LATIN_TO_PERSIAN else c for c in number])


def get_trends(time_range, limit=7):
    return session.query(Word.word, func.count(Word.id))\
        .filter(Word.time >= (datetime.now() - time_range))\
        .group_by(Word.word)\
        .order_by(desc(func.count(Word.id)))\
        .limit(limit).all()


def get_all_tweets_count(time_range):
    return session.query(func.count(Tweet.id)).filter(Tweet.time >= (datetime.now() - time_range)).scalar()


def get_trends_tweet():
    text = 'ترند در ۲۴ ساعت گذشته:\n'

    all_tweets_count = get_all_tweets_count(TIME_RANGE)

    for word, count in get_trends(TIME_RANGE):
        percentage = 100 * count / all_tweets_count

        if percentage < 3:
            continue

        to_add = '- {word} - {percentage}%\n'.format(
            word=word.encode('latin1').decode('utf-8'),
            percentage=persian_number('{:.0f}'.format(percentage))
        )

        if len(text) + len(to_add) > 160:
            break

        text += to_add

    return text


if __name__ == '__main__':
    import sys

    trends = get_trends_tweet()

    print (trends)

    if len(sys.argv) > 1 and sys.argv[1] == '--send':
        twitter_api.update_status(trends)
        print ('Sent')
