# -*- coding: UTF-8 -*-

import sys

from datetime import datetime, timedelta

from trendfa.database import session
from trendfa.models import Tweet
from sqlalchemy import desc

from trendfa.twitter import api as twitter_api


def get_most_liked(time_range):
    return session.query(Tweet)\
        .filter(Tweet.time >= (datetime.now() - time_range))\
        .order_by(desc(Tweet.likes))\
        .first()


def get_most_retweeted(time_range):
    return session.query(Tweet)\
        .filter(Tweet.time >= (datetime.now() - time_range))\
        .order_by(desc(Tweet.retweets))\
        .first()


def get_tweet_link(tweet):
    return 'https://twitter.com/anything/status/{}'.format(tweet.twitter_id)



if __name__ == '__main__':
    most_liked_tweet = get_most_liked(timedelta(days=1))
    most_retweeted_tweet = get_most_retweeted(timedelta(days=1))

    print('Most liked ({}): {}'.format(most_liked_tweet.likes, most_liked_tweet.text))
    print('Most retweeted ({}): {}'.format(most_retweeted_tweet.retweets, most_retweeted_tweet.text))

    if len(sys.argv) > 1 and sys.argv[1] == '--send-likes':
        twitter_api.update_status('بیشترین لایک در ۲۴ ساعت گذشته: \n {}'.format(get_tweet_link(most_liked_tweet)))
        print ('Sent')

    if len(sys.argv) > 1 and sys.argv[1] == '--send-retweets':
        twitter_api.update_status(
            'بیشترین ریتوییت در ۲۴ ساعت گذشته: \n {}'.format(get_tweet_link(most_retweeted_tweet))
        )
        print ('Sent')
