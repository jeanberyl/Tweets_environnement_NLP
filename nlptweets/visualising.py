import os
import re

import pandas as pd
import numpy as np
import seaborn as sns


# Visualisation function
def plot_20_most_common_words(count_data, count_vectorizer):
    import matplotlib.pyplot as plt

    words = count_vectorizer.get_feature_names()
    total_counts = np.zeros(len(words))
    for t in count_data:

        total_counts += t.toarray()[0]

    count_dict = zip(words, total_counts)
    count_dict = sorted(count_dict, key=lambda x: x[1], reverse=True)[0:20]
    words = [w[0] for w in count_dict]
    counts = [w[1] for w in count_dict]
    x_pos = np.arange(len(words))

    plt.figure(2, figsize=(15, 15 / 1.6180))
    plt.subplot(title="20 most common words")
    sns.set_context("notebook", font_scale=1.25, rc={"lines.linewidth": 2.5})
    sns.barplot(x_pos, counts, palette="husl")
    plt.xticks(x_pos, words, rotation=90)
    plt.xlabel("words")
    plt.ylabel("counts")
    plt.show()


# Visualise the 20 most common words
# plot_20_most_common_words(count_data, count_vectorizer)


# # Import the wordcloud library
# from wordcloud import WordCloud  # Join the different processed titles together.

# long_string = ",".join(
#     list(papers["paper_text_processed"].values)
# )  # Create a WordCloud object
# wordcloud = WordCloud(
#     background_color="white", max_words=5000, contour_width=3, contour_color="steelblue"
# )  # Generate a word cloud
# wordcloud.generate(long_string)  # Visualize the word cloud
# wordcloud.to_image()
