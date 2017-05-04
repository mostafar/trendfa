# -*- coding: UTF-8 -*-

import time
import tweepy
from twitter import api as twitter_api
from sqlalchemy import exists
from models import Tweet, Word
from text_analyzer import get_names
from database import session


def process_tweet(status):
    tweet = Tweet(
        twitter_id=status.id,
        text=status.text.encode('utf-8'),
        time=status.created_at,
    )

    session.add(tweet)

    for name in get_names(status.text):
        session.add(Word(
            word=name.encode('utf-8'),
            time=tweet.time,
            tweet=tweet,
        ))

    session.commit()
    session.flush()


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except (tweepy.RateLimitError, tweepy.error.TweepError) as e:
            print('RATE LIMIT, Sleeping 15 minutes')
            time.sleep(15 * 60)


if __name__ == '__main__':
    for status in limit_handled(tweepy.Cursor(twitter_api.home_timeline).items(900)):
        print('PROCESSED: {}'.format(status.id))
        if not session.query(exists().where(Tweet.twitter_id == status.id)).scalar():
            process_tweet(status)
