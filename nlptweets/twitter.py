import json
import os

import tweepy

import numpy as np
import pandas as pd

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


try:
    fpath = os.path.join(os.path.dirname(__file__), os.pardir, 'resources', 'liste_twittos_energie.csv')
    list_twittos = pd.read_csv(fpath, sep= ',')

except Exception as e:
    raise RuntimeError('Could not read csv')

print(list_twittos)

AUTH = tweepy.OAuthHandler(key1, key2)
AUTH.set_access_token(key3, key4)

TWITTER_API = tweepy.API(AUTH)

# def get_home_timeline(include_entities=True):
#     return TWITTER_API.home_timeline(include_entities=include_entities)

# def get_user_timeline(username, include_entities=True, tweet_mode='extended'):
#     return TWITTER_API.user_timeline(username, include_entities=include_entities, tweet_mode=tweet_mode)


# print(get_home_timeline())


def extract_tweet_attributes3(tweet_object):
    """ 
    Function to extract data from tweet object and put into a dataframe 
    """

    tweet_list =[]
    
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
        
    
        
        tweet_list.append({'tweet_id':tweet_id,  
                           'date': created_at,
                           'full_text': full_text,
                           'text': text, 
                           'user':user,
                           'entities':entities})



        df = pd.DataFrame(tweet_list, columns=['tweet_id',
                                                'date',
                                                'full_text',
                                                'text',
                                                'user',
                                                'entities'])
    return df    




def extract_twittos_max3600(twittos):
    """
        Function to extract tweets rom twittos list
        add dataframes in next line   
    """
    
    tweets_data_list = []
    
    for i in range(len(twittos)):
    
        ID = list_twittos['id_twitter'][i]
        
        multiple_tweets = TWITTER_API.user_timeline(ID, count = 200)
        tweets_data_list.append(multiple_tweets)
        
        while len(multiple_tweets) == 200:

            last_tweet_id = multiple_tweets[199].id

            multiple_tweets = TWITTER_API.user_timeline(ID, 
                                                count = 200, 
                                                max_id = last_tweet_id)

            tweets_data_list.append(multiple_tweets)
        

    return tweets_data_list           





# use function 
# rename var
data_list = extract_twittos_max3600(list_twittos)        

# check len
print("len data_list", len(data_list))


# say what you do and do what you say
# function "extract_tweet_attributes2" to make dataframes
# all df have same columns names, join on 

# rename var
df_list = []

# extract_tweet_attributes2(data_list[0])
for i in range(len(data_list)):
    
    df = extract_tweet_attributes3(data_list[i])
    df_list.append(df)

# check len
print("len df_list", len(df_list))

# check dims of the dataframe
table = pd.concat(df_list)
print("table shape", table.shape)

print(table.head())


try:
    fpath = os.path.join(os.path.dirname(__file__), os.pardir, 'resources', 'table_max_april28.csv')
    table.to_csv(fpath)

except Exception as e:
    raise RuntimeError('Could not write csv')