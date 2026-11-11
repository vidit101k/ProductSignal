import pandas as pd

# Load Data
df = pd.read_csv("data/data.csv")

# Data UNderstanding
print(df.shape)
print(df.dtypes)
print(df.head())
print(df.isnull().sum())
print(df.duplicated().sum())
print(df.nunique())
