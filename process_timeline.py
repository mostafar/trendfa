# -*- coding: UTF-8 -*-

import tweepy
from twitter import api as twitter_api
from sqlalchemy import exists
from models import Tweet, Word
from text_analyzer import get_names
from database import session


def process_tweet(status):
    tweet = Tweet(
        twitter_id=status.id,
        text=status.text,
        time=status.created_at,
    )

    session.add(tweet)

    for name in get_names(tweet.text):
        session.add(Word(
            word=name,
            time=tweet.time,
            tweet=tweet,
        ))

    session.commit()
    session.flush()


if __name__ == '__main__':
    for status in tweepy.Cursor(twitter_api.home_timeline).items(300):
        print(status.id)
        if not session.query(exists().where(Tweet.twitter_id == status.id)).scalar():
            process_tweet(status)
