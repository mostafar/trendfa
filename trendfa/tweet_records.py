# -*- coding: UTF-8 -*-

import sys

from datetime import datetime, timedelta

from trendfa.database import session
from trendfa.models import Tweet
from trendfa.models import Author
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


def get_best_talent(time_range):
    return session.query(Tweet)\
        .filter(Tweet.time >= (datetime.now() - time_range))\
        .filter(Tweet.likes > 50)\
        .join(Tweet.author)\
        .order_by(desc(Tweet.likes / Author.followers_count))\
        .first()


def get_tweet_link(tweet):
    return 'https://twitter.com/{}/status/{}'.format(
        tweet.author.screen_name if tweet.author_id is not None else 'anything',
        tweet.twitter_id,
    )



if __name__ == '__main__':
    most_liked_tweet = get_most_liked(timedelta(days=1))
    most_retweeted_tweet = get_most_retweeted(timedelta(days=1))
    best_talent_tweet = get_best_talent(timedelta(days=1))

    print('Most liked ({}): {}'.format(most_liked_tweet.likes, most_liked_tweet.text))
    print('Most retweeted ({}): {}'.format(most_retweeted_tweet.retweets, most_retweeted_tweet.text))
    print('Best talent ({:.2f}%): {} {}'.format(
        100.0 * best_talent_tweet.likes / best_talent_tweet.author.followers_count, 
        best_talent_tweet.twitter_id,
        best_talent_tweet.text
    ))
    
    argument = sys.argv[1] if len(sys.argv) > 1 else None

    if argument == '--send-likes':
        twitter_api.update_status('بیشترین لایک در ۲۴ ساعت گذشته: \n {}'.format(get_tweet_link(most_liked_tweet)))
        print ('Sent')

    if argument == '--send-retweets':
        twitter_api.update_status(
            'بیشترین ریتوییت در ۲۴ ساعت گذشته: \n {}'.format(get_tweet_link(most_retweeted_tweet))
        )
        print ('Sent')

    if argument == '--send-talent':
        twitter_api.update_status(
            'پدیده‌ی ۲۴ ساعت گذشته: \n {}'.format(get_tweet_link(best_talent_tweet))
        )
        print ('Sent')

