import os
import re
import ast

import pandas as pd
import numpy as np
import seaborn as sns

from datetime import date, datetime


# df = pd.read_csv("resources/table_urls_clean_topjune12.csv")
# df = df[df["full_text"].isna() == False]

# for i in range(len(df["full_text"])):
#     try:
#         if "sécuritéalimentaire" in df["full_text"].iloc[i]:
#             print(df["full_text"].iloc[i], i)
#     except:
#         pass


# for i in range(len(df["full_text"])):
#     try:
#         if "stratégiqueswashington" in df["full_text"].iloc[i]:
#             print(df["full_text"].iloc[i], i)
#     except:
#         pass


# for i in range(len(df["full_text"])):
#     try:
#         if "u4ln0a7m5r" in df["full_text"].iloc[i]:
#             print(df["full_text"].iloc[i], i)
#     except:
#         pass


# for i in range(len(df["full_text"])):
#     if "sécuritéalimentaire" in df["full_text"].iloc[i]:
#         print(df["full_text"].iloc[i])

