from pathlib import Path

import pandas as pd


def generate_titanic_data():
    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # Load the Titanic dataset from seaborn
    try:
        import seaborn as sns

        df = sns.load_dataset("titanic")
    except ImportError:
        # If seaborn is not available, use a direct URL
        url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
        df = pd.read_csv(url)

    # Save to CSV
    output_path = data_dir / "titanic.csv"
    df.to_csv(output_path, index=False)
    print(f"Titanic dataset saved to {output_path}")


if __name__ == "__main__":
    generate_titanic_data()
