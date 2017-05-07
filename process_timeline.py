# -*- coding: UTF-8 -*-

import time
import tweepy
from twitter import api as twitter_api
from models import Tweet, Word
from text_analyzer import get_names
from database import session


def process_tweet(status):
    tweet = session.query(Tweet).filter(Tweet.twitter_id == status.id).first()

    if tweet is None:
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

    tweet.likes = status.favorite_count
    tweet.retweets = status.retweet_count

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
        process_tweet(status)
