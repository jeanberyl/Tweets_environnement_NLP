import os
import re
import ast

import pandas as pd
import numpy as np

from datetime import date, datetime

pd.options.display.max_colwidth = 200

# import spacy
# # from spacy.lang.en.stop_words import STOP_WORDS
# spacy.load('fr_core_news_sm')


# from nltk.stem.snowball import FrenchStemmer
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.collocations import *

# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# stopwords = set(stopwords.words('french'))


try:
    fpath = os.path.join(
        os.path.dirname(__file__), os.pardir, "resources", "dedup_table_april28.csv"
    )
    table = pd.read_csv(fpath, sep=",", index_col=0)

except Exception as e:
    raise RuntimeError("Could not read csv")


#### fetch variables from entities json ####
table["short_url"] = np.nan
table["expanded_url"] = np.nan
table["hashtags"] = np.nan
table["symbols"] = np.nan
table["user_mentions"] = np.nan


def tryconvert(value, url_type, default):
    try:
        return ast.literal_eval(value)["urls"][0][url_type]
    except (IndexError):
        return default


table["short_url"] = table["entities"].map(lambda x: tryconvert(x, "url", "no_urls"))
table["expanded_url"] = table["entities"].map(
    lambda x: tryconvert(x, "expanded_url", "no_urls")
)

table["hashtags"] = table["entities"].map(lambda x: ast.literal_eval(x)["hashtags"])
table["symbols"] = table["entities"].map(lambda x: ast.literal_eval(x)["symbols"])
table["user_mentions"] = table["entities"].map(
    lambda x: ast.literal_eval(x)["user_mentions"]
)

#  the table saved without text cleaning
table_unclean = table

table_urls = table[table["expanded_url"] != "no_urls"]
table_unclean_urls = table_unclean[table_unclean["expanded_url"] != "no_urls"]

print("The shape of table url {a}".format(a=table_urls.shape))


# Fetch user mentions to susbtract strings
# Fetch url to substring to string

table["text"] = table.apply(
    lambda row: row["text"]
    if row["expanded_url"] == "no_urls"
    else row.text.replace(row.short_url, ""),
    axis=1,
)


#### Text processing ####


def text_cleaning():

    # remove end of line
    table["text"] = table.apply(lambda row: row.text.replace("\n", ""), axis=1)

    # Remove punctuation
    table["text"] = table["text"].map(lambda x: re.sub(r"\W+", " ", x))

    # Convert the titles to lowercase
    table["text"] = table["text"].map(lambda x: x.lower())
    return table


table = text_cleaning()

# reste les accents "conférence"


print("text before cleaning", table_unclean_urls["text"].head(10))

print("text after cleaning", table["text"].head(10))

print(table.info())

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


# # la regex est à améliorer
# h = re.compile("(.*)https")

# T_F = []
# for i in range(len(table)):

#     # check if string len is more than one character
#     try:
#         if len(h.match(table.iloc[i].enlever_retour_chariot).group(1))>1:
#             T_F.append(h.match(table.iloc[i].enlever_retour_chariot).group(1))
#         else:
#             h = re.compile(r"https:\S+(.*)")
#             T_F.append(h.match(table.iloc[i].enlever_retour_chariot).group(1))

#     except:
#         T_F.append(table.iloc[0+i].enlever_retour_chariot)

# table['text'] = T_F


# h = re.compile(r"RT @[^\s]+(.*)")

# T_F = []
# for i in range(len(table)):

#     try:
#         T_F.append(h.match(table.iloc[i].enlever_https).group(1))

#     except:
#         T_F.append(table.iloc[i].enlever_https)

# table['text'] = T_F


# nlp = spacy.load("fr_core_news_sm")


# # remove stop words

# table['paper_text_processed'] = table['paper_text_processed'].map(lambda x: ' '.join(t.text for t in nlp(x) if not t.is_stop))
# table.head()


# nlp = spacy.load("fr_core_news_sm")
# doc = nlp("C'est une phrase.")
# print([(w.text, w.pos_) for w in doc])

# df_t['word_clean1'] = df_t.apply(lambda row: list([w.lower() for w in row.lemme_rm_Stop_words if w.isalpha()]), axis=1)

# df_t['tokens_unique'] = df_t.apply(lambda row: [w.text for w in nlp(row.enlever_RT)], axis=1)

# # remove stop words
# df_t['tokens_rm_Stop_words'] = df_t.apply(lambda row: [t.text for t in nlp(row.enlever_RT) if not t.is_stop], axis=1)

# df_t['lemme_unique'] = df_t.apply(lambda row: [w.lemma_ for w in nlp(row.enlever_RT)], axis=1)

# # remove stop words
# df_t['lemme_rm_Stop_words'] = df_t.apply(lambda row: [t.lemma_ for t in nlp(row.enlever_RT) if not t.is_stop], axis=1)
