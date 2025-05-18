import pandas as pd
import ast
from langdetect import detect, LangDetectException

# read in data
df = pd.read_csv("games.csv")

# clean data
df.drop(columns=["Unnamed: 0"], inplace=True)

# convert columns to int
parse_thousand_to_int = (
    lambda x: int(1000 * float(x.split("K")[0])) if "K" in x else int(x)
)
convert_columns = [
    "Times Listed",
    "Number of Reviews",
    "Plays",
    "Playing",
    "Backlogs",
    "Wishlist",
]
for col in convert_columns:
    df[col] = df[col].apply(parse_thousand_to_int)

# remove rows with TBD release date
df = df[df["Release Date"] != "releases on TBD"]

# remove rows with any NaN values
df.dropna(inplace=True)

# remove duplicate titles
df.drop_duplicates(subset="Title", keep="first", inplace=True)

# convert columns to datetime and extract year and month
df["Release Date"] = pd.to_datetime(df["Release Date"])
df["year"] = df["Release Date"].dt.year
df["month"] = df["Release Date"].dt.month

# create a score column
df["score"] = df["Rating"] * df["Number of Reviews"]


# remove non-english reviews
df["Reviews"] = df["Reviews"].apply(ast.literal_eval)
for i in range(len(df["Reviews"])):
    for y in df["Reviews"].iloc[i]:
        try:
            if detect(y) != "en":
                df["Reviews"].iloc[i].remove(y)
        except LangDetectException:
            df["Reviews"].iloc[i].remove(y)

# save to Django app data folder
df.to_csv("../core/data/scrubbed.csv", index=False)
