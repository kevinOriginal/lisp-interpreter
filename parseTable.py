import pandas as pd
import pickle

df = pd.read_excel("./SLR_table6.xlsx", header=0, index_col=0)
df.to_dict()
df = df.T

with open("slr_table6.pickle", "wb") as f:
    pickle.dump(df, f)

print(df)