import os
import re
import ast

import pandas as pd
import numpy as np

import spacy

from datetime import date, datetime

pd.options.display.max_colwidth = 280


# from spacy.lang.en.stop_words import STOP_WORDS


# from nltk.stem.snowball import FrenchStemmer
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.collocations import *

# import nltk

# nltk.download("stopwords")
# nltk.download("punkt")
# stopwords = set(stopwords.words("french"))


try:
    fpath = os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        "resources/extract",
        "table_max_july12.csv",
    )
    table = pd.read_csv(fpath, sep=",", index_col=0)

except Exception as e:
    raise RuntimeError("Could not read csv")


#### fetch variables from entities json ####
table["short_url"] = np.nan
# table["expanded_url"] = np.nan
table["number_urls"] = table["entities"].map(lambda x: x.count("'url'"))
table["hashtags"] = np.nan
# table["symbols"] = np.nan
table["user_mentions"] = np.nan

#  adding the case with multiple urls
#  parsing urls https://docs.python.org/3/library/urllib.parse.html
# Removing RT to have feature


# def tryconvert(value, url_type, default):
#     try:
#         group = r": '(\S*)'"
#         p = re.compile(url_type + group)
#         return p.findall(str(ast.literal_eval(value)["urls"]))
#     except (IndexError):
#         return default


# def extract_user_mentions(value, default):
#     try:
#         p = re.compile(r"'screen_name': '(\S*)'")
#         return p.findall(str(ast.literal_eval(value)["user_mentions"]))
#     except (IndexError):
#         return default


# table["short_url"] = table["entities"].map(lambda x: tryconvert(x, "'url'", "no_urls"))
# table["expanded_url"] = table["entities"].map(
#     lambda x: tryconvert(x, "'expanded_url'", "no_urls")
# )

# def tryconvert(value, url_type):

#     group = r": '(\S*)'"
#     p = re.compile(url_type + group)
#     return p.findall(str(ast.literal_eval(value)["urls"]))

def tryconvert(value, url_type, default):
    try:
        group = r": '(\S*)'"
        p = re.compile(url_type + group)
        return p.findall(str(ast.literal_eval(value)["urls"]))
    except (KeyError):
        return default



def tryconvert_media(value, url_type, default):
    try:
        group = r": '(\S*)'"
        p = re.compile(url_type + group)
        return p.findall(str(ast.literal_eval(value)["media"]))
    except (KeyError):
        return default


def extract_user_mentions(value):

    p = re.compile(r"'screen_name': '(\S*)'")
    return p.findall(str(ast.literal_eval(value)["user_mentions"]))


# table["short_url"] = table["entities"].map(lambda x: tryconvert(x, "'url'"))
table["short_url"] = table["entities"].map(lambda x: tryconvert(x, "'url'", "no_urls"))

# table["expanded_url"] = table["entities"].map(
#     lambda x: tryconvert(x, "'expanded_url'", "no_urls")
# )

table["media_url"] = table["entities"].map(
    lambda x: tryconvert_media(x, "'url'", "no_media")
)
#  the default "no_urls is never used", instead it's empty list
# (len(table[table["expanded_url"] == "no_urls"]))

table["hashtags"] = table["entities"].map(lambda x: ast.literal_eval(x)["hashtags"])
#  table["symbols"] = table["entities"].map(lambda x: ast.literal_eval(x)["symbols"])
# table["user_mentions"] = table["entities"].map(
#     lambda x: ast.literal_eval(x)["user_mentions"]
# )
table["user_mentions"] = table["entities"].map(lambda x: extract_user_mentions(x))

#  the table saved without full_text cleaning
table_unclean = table


table_unclean_urls = table_unclean[table_unclean["expanded_url"] != "no_urls"]


#### full_text processing ####
def loop_erase_urls(chain, short_url):
    for i in range(len(short_url)):
        chain = chain.replace(short_url[i], "")
    return chain


# def loop_erase_user_mentions(chain, user_mentions):
#     for i in range(len(user_mentions)):
#         chain = chain.replace(user_mentions[i], "")
#     return chain


def full_text_cleaning():

    # remove end of line
    table["full_text"] = table.apply(
        lambda row: row["full_text"].replace("\n", " "), axis=1
    )

    # Fetch user mentions to susbtract strings
    # Fetch url to substring to string

    table["full_text"] = table.apply(
        lambda row: row["full_text"].replace(row.media_url, "")
        if len(table["media_url"]) != 8
        else row["full_text"],
        axis=1,
    )
    table["full_text"] = table.apply(
        lambda row: row["full_text"]
        if row["expanded_url"] == "no_urls"
        else loop_erase_urls(row["full_text"], row["short_url"]),
        axis=1,
    )

    # table["full_text"] = table.apply(
    #     lambda row: row["full_text"]
    #     if row["user_mentions"] == 2
    #     else loop_erase_user_mentions(row["full_text"], row["user_mentions"]),
    #     axis=1,
    # )

    # Remove punctuation
    table["full_text"] = table["full_text"].map(lambda x: re.sub(r"\W+", " ", x))

    # Convert the titles to lowercase
    table["full_text"] = table["full_text"].map(lambda x: x.lower())
    return table


table = full_text_cleaning()

# reste les accents "conférence"
# lemmatisation
# n-grams

# remove stop words
nlp = spacy.load("fr_core_news_sm")
table["full_text_processed"] = table["full_text"].map(
    lambda x: " ".join(t.text for t in nlp(x) if not t.is_stop)
)


print("full_text before cleaning", table_unclean_urls["full_text"].head(10))

print("full_text after cleaning", table["full_text"].head(10))

print(table.info())

#  il n'y a pas de lignes avec "no_urls"
table_urls = table[table["expanded_url"] != "no_urls"]

print("The shape of table url {a}".format(a=table_urls.shape))


try:
    fpath = os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        "resources",
        "table_urls_clean_top{a}.csv".format(
            a=datetime.strftime(date.today(), "%B%d").lower()
        ),
    )
    table_urls.to_csv(fpath)

except Exception:
    raise RuntimeError("Could not write csv")

try:
    fpath = os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        "resources",
        "table_urls_unclean_top{a}.csv".format(
            a=datetime.strftime(date.today(), "%B%d").lower()
        ),
    )
    table_unclean_urls.to_csv(fpath)

except Exception:
    raise RuntimeError("Could not write csv")


# nlp = spacy.load("en_core_web_sm")
# doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

# for token in doc:
#     print(
#         token.text,
#         token.lemma_,
#         token.pos_,
#         token.tag_,
#         token.dep_,
#         token.shape_,
#         token.is_alpha,
#         token.is_stop,
#     )

# df_t['word_clean1'] = df_t.apply(lambda row: list([w.lower() for w in row.lemme_rm_Stop_words if w.isalpha()]), axis=1)

# df_t['tokens_unique'] = df_t.apply(lambda row: [w.full_text for w in nlp(row.enlever_RT)], axis=1)

# # remove stop words
# df_t['tokens_rm_Stop_words'] = df_t.apply(lambda row: [t.full_text for t in nlp(row.enlever_RT) if not t.is_stop], axis=1)

# df_t['lemme_unique'] = df_t.apply(lambda row: [w.lemma_ for w in nlp(row.enlever_RT)], axis=1)

# # remove stop words
# df_t['lemme_rm_Stop_words'] = df_t.apply(lambda row: [t.lemma_ for t in nlp(row.enlever_RT) if not t.is_stop], axis=1)
