# import everything
from twitter import (
    import_ressources,
    import_twittos,
    extract_twittos_max3600,
    extract_tweet_attributes3,
)

import os

import numpy as np
import pandas as pd

from datetime import date, datetime


def main():
    # run your program using other defined python modules
    TWITTER_API = import_ressources()
    twittos = import_twittos()

    # use function

    # rename var
    data_list = extract_twittos_max3600(twittos, TWITTER_API)

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
            "resources/extract",
            "table_max_{a}.csv".format(
                a=datetime.strftime(date.today(), "%B%d").lower()
            ),
        )
        table.to_csv(fpath)

    except Exception:
        raise RuntimeError("Could not write csv")


if __name__ == "__main__":
    main()


def nothing():
    pass
