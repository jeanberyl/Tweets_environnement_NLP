import os
import re
import ast

import spacy

import pandas as pd
import numpy as np
import seaborn as sns

from datetime import date, datetime


from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA

import warnings

warnings.simplefilter("ignore", DeprecationWarning)


try:
    fpath = os.path.join(
        os.path.dirname(__file__), os.pardir, "resources", "table_clean_topjuly16.csv",
    )
    table = pd.read_csv(fpath, sep=",", index_col=0)

except Exception as e:
    raise RuntimeError("Could not read csv")


print(table.columns)


# ###### Vectorizing #######

table["full_text_processed"] = table["full_text_processed"].values.astype("U")


count_vectorizer = CountVectorizer()  # Fit and transform the processed titles
count_data = count_vectorizer.fit_transform(table["full_text_processed"])

# Helper function
def print_topics(model, count_vectorizer, n_top_words):
    words = count_vectorizer.get_feature_names()
    for topic_idx, topic in enumerate(model.components_):
        print("\nTopic #%d:" % topic_idx)
        print(" ".join([words[i] for i in topic.argsort()[: -n_top_words - 1 : -1]]))


# Tweak the two parameters below
number_topics = 15
number_words = 200  # Create and fit the LDA model
lda = LDA(n_components=number_topics, n_jobs=-1)
lda.fit(count_data)  # Print the topics found by the LDA model
print("Topics found via LDA:")
print_topics(lda, count_vectorizer, number_words)


#  tokens uniques
# vectorizer = CountVectorizer()
# X = vectorizer.fit_transform(table["full_text_processed"])
# print(vectorizer.get_feature_names())


# vectorizer = TfidfVectorizer()
# X = vectorizer.fit_transform(table["full_text_processed"])
# print(vectorizer.get_feature_names())
# print(X.shape)

# tfidf_df = pd.DataFrame(X)

# try:
#     fpath = os.path.join(
#         os.path.dirname(__file__),
#         os.pardir,
#         "resources",
#         "X{a}.csv".format(a=datetime.strftime(date.today(), "%B%d").lower()),
#     )
#     tfidf_df.to_csv(fpath)

# except Exception:
#     raise RuntimeError("Could not write csv")


# # #SUR LES LEMS
# # #Ici le calcul des descripteurs est uniquement exploratoire, il s'agit de faire ressortir les associations de mots fréquentes afin de fusionner celles qui forment une expression sensée

# # #Matrice des bigrams (association de deux mots)
# # vect_count_bigrams = CountVectorizer(min_df=5, ngram_range=(2,2)).fit(dff['lemmas'])
# # lem_gram_vect = vect_count_bigrams.transform(dff['lemmas'])
# # lem_gram = pd.DataFrame(lem_gram_vect.todense()).rename(columns=renomecol(vect_count_bigrams))

# # #Matrice des trigrams (association de trois mots)
# # vect_count_trigrams = CountVectorizer(min_df=1, ngram_range=(3,3)).fit(dff['lemmas'])
# # lem_trigram_vect = vect_count_trigrams.transform(dff['lemmas'])
# # lem_trigram = pd.DataFrame(lem_trigram_vect.todense()).rename(columns=renomecol(vect_count_trigrams))
