# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta
from collections import defaultdict
import itertools

from trendfa.database import session
from trendfa.models import Tweet
from trendfa.text_analyzer import get_names
from sqlalchemy import desc
from sqlalchemy import func

from trendfa.twitter import api as twitter_api

TIME_RANGE = timedelta(days=1)
LATIN_TO_PERSIAN = {latin: persian for latin, persian in [('0', '۰'), ('1', '۱'), ('2', '۲'), ('3', '۳'), ('4', '۴'), ('5', '۵'), ('6', '۶'), ('7', '۷'), ('8', '۸'), ('9', '۹'),]}


def persian_number(number):
    number = str(number)
    return ''.join([LATIN_TO_PERSIAN[c] if c in LATIN_TO_PERSIAN else c for c in number])


def get_tweet_texts(time_range):
    return [
        result[0] for result in 
        session.query(Tweet.text)
            .filter(Tweet.time >= (datetime.now() - time_range))
            .all()
    ]


def get_words(tweet_texts):
    print(tweet_texts[:10])

    return itertools.chain(*[get_names(tweet_text) for tweet_text in tweet_texts])


def get_trends(time_range, limit=7):
    words_count = defaultdict(int)
    for word in get_words(get_tweet_texts(time_range)):
        words_count[word] += 1
    return sorted(words_count.items(), key=lambda t: t[1], reverse=True)[:limit]


def get_all_tweets_count(time_range):
    return session.query(func.count(Tweet.id)).filter(Tweet.time >= (datetime.now() - time_range)).scalar()


def get_trends_tweet():
    text = 'ترند در ۲۴ ساعت گذشته:\n'

    all_tweets_count = get_all_tweets_count(TIME_RANGE)

    trends = [(word, round(100.0 * count / all_tweets_count)) for word, count in get_trends(TIME_RANGE)]
    qualified_trends = [(word, percentage) for index, (word, percentage) in enumerate(trends) if index < 3 or percentage >= 3 - 0.001]

    if len(qualified_trends) == 0:
        return None

    for word, percentage in qualified_trends:
        to_add = '- {word} - {percentage}%\n'.format(
            word=word,
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

    if len(sys.argv) > 1 and sys.argv[1] == '--send' and trends is not None:
        twitter_api.update_status(trends)
        print ('Sent')

