# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta
from collections import defaultdict
import itertools

from trendfa.database import session
from trendfa.models import Tweet
from trendfa.tweet_trends import get_tweet_texts
from trendfa.text_analyzer import get_hash_tags
from sqlalchemy import desc
from sqlalchemy import func

from trendfa.twitter import api as twitter_api

TIME_RANGE = timedelta(days=1)


def get_all_hashtags(tweet_texts):
    return itertools.chain(*[get_hash_tags(tweet_text) for tweet_text in tweet_texts])


def get_hashtag_trends(time_range, limit=3):
    hashtags = defaultdict(int)
    for hashtag in get_all_hashtags(get_tweet_texts(time_range)):
        hashtags[hashtag] += 1
    return sorted(hashtags.items(), key=lambda t: t[1], reverse=True)[:limit]


def get_trends_tweet():
    return 'هشتگ‌های پر‌طرفدار:\n\n{trends}'.format(
        trends='\n'.join(
            '- {word}'.format(word=word) for word, count in get_hashtag_trends(TIME_RANGE)
        )
    )


if __name__ == '__main__':
    import sys

    trends = get_trends_tweet()

    print (trends)

    if len(sys.argv) > 1 and sys.argv[1] == '--send' and trends is not None:
        twitter_api.update_status(trends)
        print ('Sent')

