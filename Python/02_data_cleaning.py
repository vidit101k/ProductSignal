import pandas as pd

# Load Data
df = pd.read_csv("data/data.csv")
print("Original shape:",df.shape)

# Remove dupliactes
df = df.drop_duplicates()
print("shape after removing duplicates:",df.shape)

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ","_")

# Convert date column
df["date"] = pd.to_datetime(df["date"], errors="coerce")
print("Invalid dates:", df["date"].isnull().sum())

# Check missing values
print("Missing values:")
print(df.isnull().sum())

# Check negative financial values
print("Negative order values:", (df["order_value"] < 0).sum())
print("Negative revenue:", (df["revenue"] < 0).sum())

# Check funnel columns
funnel_columns = ["visited_website",
                  "viewed_product",
                  "added_to_cart",
                  "checkout_started",
                  "purchase_completed"
                  ]

print("Funnel value counts:")

for column in funnel_columns:
    print(f"{column}")
    print(df[column].value_counts())

# Check logical funnel violations

# Product viewed without visiting website
violation_1 = (
    (df["viewed_product"] == 1) &
    (df["visited_website"] == 0)
).sum()

# Added to cart without viewing product
violation_2 = (
    (df["added_to_cart"] == 1) &
    (df["viewed_product"] == 0)
).sum()

# Checkout without adding to cart
violation_3 = (
    (df["checkout_started"] == 1) &
    (df["added_to_cart"] == 0)    
).sum()

# Purchase without checkout
violation_4 = (
    (df["purchase_completed"] == 1) &
    (df["checkout_started"] == 0)
).sum()

print("FUNNEL LOGIC CHECK")
print("Viewed product without website visit:",violation_1)
print("Added to cart without viewing product:",violation_2)
print("Checkout without adding to cart:",violation_3)
print("Purchase without checkout:",violation_4)

# Save cleaned data
df.to_csv("data/cleaned_data.csv", index=False)

print("Cleaned dataset saved successfully.")
print("Final shape:", df.shape)

