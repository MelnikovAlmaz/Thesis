import pandas as pd


data_df = pd.read_csv("../../../data/user.csv", sep=';')

print(data_df.iloc[0])