import ast
import os
import re
import time


import spacy

import pandas as pd
import numpy as np


from datetime import date, datetime


from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np

from pandas.io.json import json_normalize
from nltk.tokenize import TweetTokenizer
from pprint import pprint

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy pour lemmatization
import spacy

# Importer la liste de stopword NLTK
import nltk; nltk.download('stopwords'); nltk.download("words")
from nltk.corpus import wordnet
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
# Ajouter certains stopwords en fonction du corpus de données si nécessaire
stop_words.extend(['rt',])



from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA

import warnings

warnings.simplefilter("ignore", DeprecationWarning)

# df = pd.read_csv("resources/table_clean_topjuly16.csv", index_col = 0)

# df.head()
# df = pd.read_csv("../resources/table_clean_topjuly16.csv", index_col = 0)

# df.head()
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



count_vectorizer = CountVectorizer(ngram_range=(1, 2))# Fit and transform the processed titles
count_data = count_vectorizer.fit_transform(table["full_text_processed"])# Visualise the 10 most common words
 
        
# Tweak the two parameters below
number_topics = 15
number_words = 200# Create and fit the LDA model
lda = LDA(n_components=number_topics, n_jobs=-1)
lda.fit(count_data)# Print the topics found by the LDA model



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
