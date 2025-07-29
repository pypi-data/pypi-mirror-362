#!/usr/local/bin/python3

# https://campus.datacamp.com/courses/data-manipulation-with-pandas/transforming-data?ex=2

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import (
    SelectFdr,
    SelectFpr,
    SelectFwe,
    SelectKBest,
    chi2,
    f_classif,
)
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

X, y = make_classification(
    n_samples=100, n_features=6, n_informative=3, n_redundant=3, random_state=123
)

df = (
    pd.DataFrame(X, y)
    .reset_index()
    .rename(
        columns={
            "index": "label",
            0: "feature_0",
            1: "feature_1",
            2: "feature_2",
            3: "feature_3",
            4: "feature_4",
            5: "feature_5",
        }
    )
)


# print(df.head())
# print(df.info())
# print(df.shape)
# print(df.describe())
