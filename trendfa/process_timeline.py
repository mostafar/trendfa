# -*- coding: UTF-8 -*-

import time
import json

import tweepy

from dateutil import parser as datetime_parser

from settings import TWEETS_LANG

from trendfa.database import session
from trendfa.models import Author, Tweet
from trendfa.text_analyzer import get_names

from trendfa.twitter import api as twitter_api

MAX_TWEETS_TO_PROCESS_COUNT = 800


def process_tweet(status):
    if 'retweeted_status' in status:
        print ('Skipping retweet')
        process_tweet(status['retweeted_status'])
        return

    if status['lang'] != TWEETS_LANG:
        print('This is not persian :(')
        return
   
    if 'quoted_status' in status:
        print ('Processing quoted tweet')
        process_tweet(status['quoted_status'])

    author = session.query(Author).filter(Author.twitter_id == status['user']['id_str']).first()

    if author is None:
        author = Author(
            twitter_id=status['user']['id_str'],
            screen_name=status['user']['screen_name'],
            followers_count=status['user']['followers_count'],
        )

        session.add(author)

    author.screen_name = status['user']['screen_name']
    author.followers_count = status['user']['followers_count']

    session.flush()

    tweet = session.query(Tweet).filter(Tweet.twitter_id == status['id']).first()

    if tweet is None:
        tweet = Tweet(
            twitter_id=status['id'],
            text=status['text'],
            time=datetime_parser.parse(status['created_at']),
            author=author,
        )

        session.add(tweet)

    tweet.likes = status['favorite_count']
    tweet.retweets = status['retweet_count']

    session.commit()

    if not status['user']['following']:
        print ('Not following, following {}'.format(status['user']['screen_name']))
        twitter_api.create_friendship(id=status['user']['id'])


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except (tweepy.RateLimitError, tweepy.error.TweepError) as e:
            print('RATE LIMIT, Sleeping 15 minutes')
            time.sleep(15 * 60)


def process_timeline():
    while (True):
        try:
            statuses = twitter_api.home_timeline(count=MAX_TWEETS_TO_PROCESS_COUNT)
        except (tweepy.RateLimitError, tweepy.error.TweepError) as e:
            print('RATE LIMIT, Sleeping 15 minutes')
            time.sleep(15 * 60)
            continue

        print ('Fetched {} tweets ...'.format(len(statuses)))
        with open('tweets.log', 'a') as log_file:
            for status in statuses:
                log_file.write('{}\n'.format(json.dumps(status._json)))
                process_tweet(status._json)
                print('PROCESSED: {}'.format(status.id))

        time.sleep(1 * 60)


if __name__ == '__main__':
    process_timeline()
