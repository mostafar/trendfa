# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta

from database import session
from models import Word, Tweet
from twitter import api as twitter_api


def get_most_liked(time_range):
    return session.query(Tweet)\
        .filter(Tweet.time >= (datetime.now() - time_range))\
        .order_by(Tweet.likes)\
        .first()


def get_most_retweeted(time_range):
    return session.query(Tweet)\
        .filter(Tweet.time >= (datetime.now() - time_range))\
        .order_by(Tweet.retweets)\
        .first()


def get_tweet_link(tweet):
    return 'https://twitter.com/anything/status/{}'.format(tweet.twitter_id)


def tweet_records(most_liked_tweet, most_retweeted_tweet):
    twitter_api.update_status('بیشترین لایک در ۲۴ ساعت گذشته: \n {}'.format(get_tweet_link(most_liked_tweet)))
    twitter_api.update_status('بیشترین ریتوییت در ۲۴ ساعت گذشته: \n {}'.format(get_tweet_link(most_retweeted_tweet)))


if __name__ == '__main__':
    most_liked_tweet = get_most_liked(timedelta(days=2))
    most_retweeted_tweet = get_most_retweeted(timedelta(days=2))

    print('Most liked ({}): {}'.format(most_liked_tweet.likes, most_liked_tweet.text))
    print('Most retweeted ({}): {}'.format(most_retweeted_tweet.retweets, most_retweeted_tweet.text))

    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--send':
        tweet_records(most_liked_tweet, most_retweeted_tweet)
        print ('Sent')
