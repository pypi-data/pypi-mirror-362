from pathlib import Path
import seaborn as sns
import pandas as pd


Path(__file__).resolve().parent.parent.joinpath("data").mkdir(exist_ok=True)
df = sns.load_dataset("titanic")
df.to_csv(f"data/titanic.csv", index=False)

