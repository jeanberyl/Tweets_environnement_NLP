import os
import re
import ast

import pandas as pd
import numpy as np
import seaborn as sns

# ###### Vectorizing #######


# # tokens uniques
# vectorizer = CountVectorizer()
# vectorizer.fit_transform(df_t.enlever_RT)
# print(vectorizer.get_feature_names())


# vectorizer = TfidfVectorizer()
# X = vectorizer.fit_transform(df_t.enlever_RT)
# # print(vectorizer.get_feature_names())
# print(X.shape)

# # Initialise the count vectorizer with the English stop words
# count_vectorizer = CountVectorizer()


# # Fit and transform the processed titles
# count_data = count_vectorizer.fit_transform(corpus['paper_text_processed'])

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