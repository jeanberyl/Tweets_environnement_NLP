import os

import pandas as pd


def dedup_tweets():
    """ 
    function to de duplicate tweets in order append new tweets to old tweets to grow the tweet dataframe 
    """

    try:
        fpath = os.path.join(os.path.dirname(__file__), os.pardir, 'resources', 'table_max_dec20.csv')
        old_table = pd.read_csv(fpath, sep= ',', index_col=0)

    except Exception as e:
        raise RuntimeError('Could not read csv')

    print("len old_table", len(old_table))
    print(old_table.head())


    try:
        fpath = os.path.join(os.path.dirname(__file__), os.pardir, 'resources', 'table_max_april28.csv')
        new_table = pd.read_csv(fpath, sep= ',', index_col=0)

    except Exception as e:
        raise RuntimeError('Could not read csv')

    print("len new_table", len(new_table))

    dedup_table = pd.concat([old_table, new_table])
    dedup_table.drop_duplicates(inplace=True)

    print("len dedup_table", len(dedup_table))

    try:
        fpath = os.path.join(os.path.dirname(__file__), os.pardir, 'resources', 'dedup_table_april28.csv')
        dedup_table.to_csv(fpath)

    except Exception as e:
        raise RuntimeError('Could not write csv')



dedup_tweets()