#!/usr/local/bin/python3

# https://campus.datacamp.com/courses/supervised-learning-with-scikit-learn/

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pydataset import data
from scipy.stats import randint
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    cross_val_score,
    train_test_split,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

df = data("diamonds")
df["price_cat"] = np.where(df["price"] > 17000, 1, 0)

X = df[["depth", "x", "y", "z"]].values
y = df["price_cat"].values

param_dist = {
    "max_depth": [3, None],
    "max_features": randint(1, 4),
    "min_samples_leaf": randint(1, 9),
    "criterion": ["gini", "entropy"],
}

tree = DecisionTreeClassifier()

tree_cv = RandomizedSearchCV(tree, param_dist, cv=5)

tree_cv.fit(X, y)

print("Tuned parameters:", tree_cv.best_params_)
print("Best score:", tree_cv.best_score_)
