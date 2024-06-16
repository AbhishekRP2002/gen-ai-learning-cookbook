import modin.pandas as pd
from rich.pretty import pprint

pd.set_option("display.max_columns", None)

if __name__ == "__main__":
    df = pd.read_csv("data/podcastdata_dataset.csv")
    cols = df.columns
    # df = df.drop(columns=[cols[0]])
    # df.to_csv("data/podcastdata_dataset.csv", index=False)
    pprint(df.head())
