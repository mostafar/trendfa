# -*- coding: UTF-8 -*-

import time
import json

import tweepy

from settings import TWEETS_LANG

from trendfa.database import session
from trendfa.models import Author, Tweet, Word
from trendfa.text_analyzer import get_names

from trendfa.twitter import api as twitter_api

TWEETS_TO_PROCESS_COUNT = 1500


def process_tweet(status):
    with open('tweets.log', 'a') as log_file:
        log_file.write('{}\n'.format(json.dumps(status._json)))

    if status.lang != TWEETS_LANG:
        print('This is not persian :(')
        return

    author = session.query(Author).filter(Author.twitter_id == status.author.id_str).first()

    if author is None:
        author = Author(
            twitter_id=status.author.id_str,
            screen_name=status.author.screen_name,
            followers_count=status.author.followers_count,
        )

        session.add(author)

    author.screen_name = status.author.screen_name
    author.followers_count = status.author.followers_count

    session.commit()

    tweet = session.query(Tweet).filter(Tweet.twitter_id == status.id).first()

    if tweet is None:
        tweet = Tweet(
            twitter_id=status.id,
            text=status.text.encode('utf-8'),
            time=status.created_at,
            author=author,
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
    for status in limit_handled(tweepy.Cursor(twitter_api.home_timeline).items(TWEETS_TO_PROCESS_COUNT)):
        print('PROCESSED: {}'.format(status.id))
        process_tweet(status)
