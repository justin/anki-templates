import pandas as pd

vocab = pd.read_csv(
    "./src/data/Vocabulary.csv",
    header=0,
    keep_default_na=False,
    na_values=[""])
vocab.set_index('guid', inplace=True)
vocab = vocab[["expression", "meaning"]]
vocab = vocab[vocab["meaning"].str.startswith('to ')]

verbs = pd.read_csv(
    "./src/data/Verb Conjugations.csv",
    header=0,
    keep_default_na=False,
    na_values=[""])
verbs.set_index('guid', inplace=True)

values_list = set(verbs["expression"])
missing_verbs = vocab[~vocab["expression"].isin(values_list)]

result = pd.concat([verbs, missing_verbs], ignore_index=False)
result = result.drop_duplicates()

result.to_csv("./src/data/Verb Conjugations.csv")
