import json
import os

import tweepy

import numpy as np
import pandas as pd

from datetime import date, datetime


def import_ressources():

    try:
        fpath = os.path.join(
            os.path.dirname(__file__), os.pardir, "resources", "credentials.json"
        )
        with open(fpath) as fobj:
            keys = json.load(fobj)
            key1 = keys["key1"]
            key2 = keys["key2"]
            key3 = keys["key3"]
            key4 = keys["key4"]
    except Exception as e:
        raise RuntimeError(
            "Could not read keys from credentials file. {a} {b}".format(
                a=repr(e), b=fpath
            )
        )

    AUTH = tweepy.OAuthHandler(key1, key2)
    AUTH.set_access_token(key3, key4)

    return tweepy.API(AUTH)

# GLOBAL VARIABLE - BAD
TWITTER_API = import_ressources()


def import_twittos():
    try:
        fpath = os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            "resources",
            "liste_twittos_energie.csv",
        )
        list_twittos = pd.read_csv(fpath, sep=",")

    except Exception:
        raise RuntimeError("Could not read csv")

    print(list_twittos)
    return list_twittos

# GLOBAL VARIABLE - BAD
twittos = import_twittos()

def extract_tweet_attributes3(tweet_object):
    """ 
    Function to extract data from tweet object and put into a dataframe 
    """

    tweet_list = []

    for tweet in tweet_object:

        tweet_id = tweet.id
        created_at = tweet.created_at
        try:
            full_text = tweet.full_text
        except:
            full_text = np.nan
        try:
            text = tweet.text
        except:
            text = np.nan
        user = tweet.user.screen_name
        entities = tweet.entities

        tweet_list.append(
            {
                "tweet_id": tweet_id,
                "date": created_at,
                "full_text": full_text,
                "text": text,
                "user": user,
                "entities": entities,
            }
        )
        df = pd.DataFrame(
            tweet_list,
            columns=["tweet_id", "date", "full_text", "text", "user", "entities"],
        )
    return df


def extract_twittos_max3600(twittos):
    """
        Function to extract tweets from twittos list
        add dataframes in next line   
    """

    tweets_data_list = []

    for i in range(len(twittos)):

        ID = twittos["id_twitter"][i]

        multiple_tweets = TWITTER_API.user_timeline(ID, count=200)
        tweets_data_list.append(multiple_tweets)

        while len(multiple_tweets) == 200:

            last_tweet_id = multiple_tweets[199].id

            multiple_tweets = TWITTER_API.user_timeline(
                ID, count=200, max_id=last_tweet_id
            )

            tweets_data_list.append(multiple_tweets)

    return tweets_data_list


# use function
# rename var
data_list = extract_twittos_max3600(twittos)

# check len
print("len data_list", len(data_list))


# rename var
df_list = []

# make one big df of the extracted tweets
for i in range(len(data_list)):

    df = extract_tweet_attributes3(data_list[i])
    df_list.append(df)

# check len
print("len df_list", len(df_list))

# check dims of the dataframe
table = pd.concat(df_list)
print("table shape", table.shape)

print(table.head())


##### write the file with current date #####


try:
    fpath = os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        "resources",
        "table_max_{a}.csv".format(a=datetime.strftime(date.today(), "%B%d").lower()),
    )
    table.to_csv(fpath)

except Exception:
    raise RuntimeError("Could not write csv")
