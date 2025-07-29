from datetime import date
from pathlib import Path

import pandas as pd

df = pd.read_csv("data/penguins.csv")

plt = df.plot.hist().get_figure()
folder_to_log = "./out/"
Path(folder_to_log).mkdir(parents=True, exist_ok=True)
plt.savefig(folder_to_log + f'{date.today().strftime("%Y%m%d")}_plot.pdf')

# todo, bv: create evaluation plots, shap, etc.


# q: how to save the model?
# a: https://scikit-learn.org/stable/modules/model_persistence.html


# write function to save model
def save_model():
    """
    function to save model
    :return:
    :rtype:
    """
