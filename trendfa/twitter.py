import tweepy
import secrets

auth = tweepy.OAuthHandler(secrets.API_KEY, secrets.API_SECRET)
auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
