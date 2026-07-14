import pandas as pd

data = pd.read_csv("data/real_phishing_urls.csv")

print("Dataset shape:")
print(data.shape)

print("\nColumn names:")
print(data.columns.tolist())

print("\nFirst 5 rows:")
print(data.head())

print("\nMissing values:")
print(data.isnull().sum())