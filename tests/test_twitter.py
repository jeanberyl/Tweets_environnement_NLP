# from Tweets_environnement_NLP.nlptweets import twitter
# import unittest

from nlptweets.twitter import import_ressources


# check twittos are in a list
# check size in extract twittos
# check columns in extract attributes

TWITTER_API = import_ressources()




def test_api():
    assert TWITTER_API.get_user_timeline('NicolasMeilhan') == 6

# def get_user_timeline(username, include_entities=True, tweet_mode='extended'):
#     return TWITTER_API.user_timeline(username, include_entities=include_entities, tweet_mode=tweet_mode)

