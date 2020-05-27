# from Tweets_environnement_NLP.nlptweets import twitter
# python -m pytest tests/

from nlptweets.twitter import (
    import_ressources,
    import_twittos,
    extract_twittos_max3600,
    extract_tweet_attributes3,
)

import os
import pickle

import pandas as pd

# check twittos are in a list
# check size in extract twittos


TWITTER_API = import_ressources()
twittos = import_twittos()
print(len(TWITTER_API.user_timeline("NicolasMeilhan")))

tweets_data_list_extracted = extract_twittos_max3600(twittos, TWITTER_API)
print("len tweets_data_list", len(tweets_data_list_extracted))


# check columns in extract attributes
# read the saved tweets object
try:
    fpath = os.path.join(
        os.path.dirname(__file__), os.pardir, "resources", "tweets_data_list_pckl",
    )
    with open(fpath, "rb") as fp:
        tweets_data_list_save = pickle.load(fp)


except Exception:
    raise RuntimeError("Could not read pickle file")

# rename var
df_list = []

# make one big df of the extracted tweets
for i in range(len(tweets_data_list_save)):

    df = extract_tweet_attributes3(tweets_data_list_save[i])
    df_list.append(df)

table = pd.concat(df_list)

print("{a} lines and {b} columns".format(a=table.shape[0], b=table.shape[1]))


def test_api():
    assert len(TWITTER_API.user_timeline("NicolasMeilhan")) > 0


def test_twittos():
    assert len(twittos) == 5


def test_extract_twittos_3600():
    assert len(tweets_data_list_extracted) > 40


def test_extract_tweet_attributes3():
    assert table.shape[0] > 4000
    assert table.shape[1] == 6
