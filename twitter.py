import tweepy


API_KEY = 'F6zX8Mys4KHJFAspxvgLoBXaQ'
API_SECRET = 'ewmchxgry11fxB0XkVBY0hWEsDVsvDBiPmPiaz4em9Mm1G4EWN'
ACCESS_TOKEN = '858126433746550784-NTAGrP7u5pde00WEaY4cX3AwSN8RYyG'
ACCESS_TOKEN_SECRET = 'mjHTKQVdvnE3DK30DQjPQWpwkgfekPb0QK7BRLXy03Rsu'

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
