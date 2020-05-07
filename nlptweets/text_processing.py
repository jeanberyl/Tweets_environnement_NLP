import os
import re

import pandas as pd
import numpy as np
# import spacy
# # from spacy.lang.en.stop_words import STOP_WORDS
# spacy.load('fr_core_news_sm')

# from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
# from sklearn.decomposition import LatentDirichletAllocation as LDA

# from nltk.stem.snowball import FrenchStemmer
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.collocations import *

# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# stopwords = set(stopwords.words('french'))

# import matplotlib.pyplot as plt
# import seaborn as sns
# sns.set_style('whitegrid')



try:
    fpath = os.path.join(os.path.dirname(__file__), os.pardir, 'resources', 'dedup_table_april28.csv')
    table = pd.read_csv(fpath,sep= ',', index_col=0)

except Exception as e:
    raise RuntimeError('Could not read csv')


print(table.head())

print(table.info())


# old table
try:
    fpath = os.path.join(os.path.dirname(__file__), os.pardir, 'resources', 'table_max_dec20.csv')
    table_old = pd.read_csv(fpath,sep= ',', index_col=0)

except Exception as e:
    raise RuntimeError('Could not read csv')


print(table_old.head())

print(table_old.info())

# fetch url shared (NicolasMeilhan_tweets[0].entities)['urls'][0]['expanded_url']
# fetch hashtags (NicolasMeilhan_tweets[0].entities)['hashtags']


table['enlever_retour_chariot'] = table.apply(lambda row: row.text.replace('\n', ""), axis=1)
table.head()


# la regex est à améliorer
h = re.compile("(.*)https")                   
 
T_F = []
for i in range(len(table)):
    
    # check if string len is more than one character
    try: 
        if len(h.match(table.iloc[i].enlever_retour_chariot).group(1))>1:
            T_F.append(h.match(table.iloc[i].enlever_retour_chariot).group(1))
        else:
            h = re.compile("https:\S+(.*)")
            T_F.append(h.match(table.iloc[i].enlever_retour_chariot).group(1))
            
    except: 
        T_F.append(table.iloc[0+i].enlever_retour_chariot)

table['enlever_https'] = T_F
table.head()


h = re.compile("RT @[^\s]+(.*)")

T_F = []
for i in range(len(table)):

    try: 
        T_F.append(h.match(table.iloc[i].enlever_https).group(1))
        
    except:
        T_F.append(table.iloc[i].enlever_https)

table['enlever_RT'] = T_F
table.head()


# Remove punctuation
table['paper_text_processed'] = table['enlever_RT'].map(lambda x: re.sub('\W+',' ', x ))
table.head()


# Convert the titles to lowercase
table['paper_text_processed'] = table['paper_text_processed'].map(lambda x: x.lower())
table.head()


nlp = spacy.load("fr_core_news_sm")



# remove stop words

table['paper_text_processed'] = table['paper_text_processed'].map(lambda x: ' '.join(t.text for t in nlp(x) if not t.is_stop))
table.head()





nlp = spacy.load("fr_core_news_sm")
doc = nlp("C'est une phrase.")
print([(w.text, w.pos_) for w in doc])

df_t['word_clean1'] = df_t.apply(lambda row: list([w.lower() for w in row.lemme_rm_Stop_words if w.isalpha()]), axis=1)

df_t['tokens_unique'] = df_t.apply(lambda row: [w.text for w in nlp(row.enlever_RT)], axis=1)

# remove stop words
df_t['tokens_rm_Stop_words'] = df_t.apply(lambda row: [t.text for t in nlp(row.enlever_RT) if not t.is_stop], axis=1)

df_t['lemme_unique'] = df_t.apply(lambda row: [w.lemma_ for w in nlp(row.enlever_RT)], axis=1)

# remove stop words
df_t['lemme_rm_Stop_words'] = df_t.apply(lambda row: [t.lemma_ for t in nlp(row.enlever_RT) if not t.is_stop], axis=1)



###### Vectorizing #######


# tokens uniques
vectorizer = CountVectorizer()
vectorizer.fit_transform(df_t.enlever_RT)
print(vectorizer.get_feature_names())


vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df_t.enlever_RT)
# print(vectorizer.get_feature_names())
print(X.shape)

# Initialise the count vectorizer with the English stop words
count_vectorizer = CountVectorizer()


# Fit and transform the processed titles
count_data = count_vectorizer.fit_transform(corpus['paper_text_processed'])

# #SUR LES LEMS
# #Ici le calcul des descripteurs est uniquement exploratoire, il s'agit de faire ressortir les associations de mots fréquentes afin de fusionner celles qui forment une expression sensée

# #Matrice des bigrams (association de deux mots)
# vect_count_bigrams = CountVectorizer(min_df=5, ngram_range=(2,2)).fit(dff['lemmas'])
# lem_gram_vect = vect_count_bigrams.transform(dff['lemmas'])
# lem_gram = pd.DataFrame(lem_gram_vect.todense()).rename(columns=renomecol(vect_count_bigrams))

# #Matrice des trigrams (association de trois mots)
# vect_count_trigrams = CountVectorizer(min_df=1, ngram_range=(3,3)).fit(dff['lemmas'])
# lem_trigram_vect = vect_count_trigrams.transform(dff['lemmas'])
# lem_trigram = pd.DataFrame(lem_trigram_vect.todense()).rename(columns=renomecol(vect_count_trigrams))