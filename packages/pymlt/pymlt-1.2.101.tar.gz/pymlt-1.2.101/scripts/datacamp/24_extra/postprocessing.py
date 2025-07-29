#!/usr/local/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from imblearn.over_sampling import RandomOverSampler
from pandas.api.types import is_numeric_dtype, is_string_dtype
from pydataset import data
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split

df = data("diamonds").reset_index(drop=True)
df["label"] = df["price"] > 15_000
print(df.head())


for c in df.columns:
    print(c)
    if is_string_dtype(df[c]):
        df_grouped = df.groupby(c).label.agg(["mean"]).reset_index()
    if is_numeric_dtype(df[c]):
        df[c] = round(df[c])
        df_grouped = df.groupby(c).label.agg(["mean"]).reset_index()
    g = sns.lineplot(
        data=df_grouped, x=c, y="mean", linewidth=1, markersize=3, marker="o"
    )
    g.axhline(0, linewidth=0.5, c="gray")
    g.set(xlabel=None, ylabel=None)
    g.tick_params(labelsize=7)
    plt.title(c, size=7)
    plt.show()
