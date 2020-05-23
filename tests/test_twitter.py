# from Tweets_environnement_NLP.nlptweets import twitter
import unittest

from twitter import import_ressources


# if __name__ == "__main__":

#     print("Found key 1: {}".format(twitter.key1))
#     print("Found key 2: {}".format(twitter.key2))
#     print("Found key 3: {}".format(twitter.key3))
#     print("Found key 4: {}".format(twitter.key4))

#  check twittos are in a list
#  check size in extract twittos
# check columns in extract attributes


# class TestSum(unittest.TestCase):
#     def test_sum(self):
#         self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

#     def test_sum_tuple(self):
#         self.assertEqual(sum((1, 3, 2)), 6, "Should be 6")

TWITTER_API = import_ressources()


class TestTwitter(unittest.TestCase):
    def test_import_ressources(self):

        self.assertEqual(
            TWITTER_API.get_user_timeline(NicolasMeilhan), 6, "Should be 6"
        )

    # def test_import_twittos(self):
    #     self.assertEqual(), 6, "Should be 6")


# def get_user_timeline(username, include_entities=True, tweet_mode='extended'):
#     return TWITTER_API.user_timeline(username, include_entities=include_entities, tweet_mode=tweet_mode)


if __name__ == "__main__":
    unittest.main()
