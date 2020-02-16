import json
import os

import tweepy

try:
    fpath = os.path.join(os.path.dirname(__file__), os.pardir, 'resources', 'credentials.json')
    with open(fpath) as fobj:
        keys = json.load(fobj)
        key1 = keys['key1']
        key2 = keys['key2']
        key3 = keys['key3']
        key4 = keys['key4']
except Exception as e:
    raise RuntimeError('Could not read keys from credentials file. {a} {b}'.format(a=repr(e), b=fpath))

AUTH = tweepy.OAuthHandler(key1, key2)
AUTH.set_access_token(key3, key4)

TWITTER_API = tweepy.API(AUTH)

def get_home_timeline(include_entities=True):
    return TWITTER_API.home_timeline(include_entities=include_entities)

def get_user_timeline(username, include_entities=True, tweet_mode='extended'):
    return TWITTER_API.user_timeline(username, include_entities=include_entities, tweet_mode=tweet_mode)