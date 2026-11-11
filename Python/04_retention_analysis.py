import pandas as pd

# Load cleaned data
df = pd.read_csv("data/cleaned_data.csv")

# Convert date
df["date"] = pd.to_datetime(df["date"])

# Keep only completed purchases
purchases = df[df["purchase_completed"].str.lower() == "yes"].copy()

print("Total purchase sessions:", len(purchases))
print("Unique purchasing users:", purchases["user_id"].nunique())

# First each user's first purchase
first_purchase = (
    purchases.groupby("user_id")["date"]
    .min()
    .reset_index()
)

first_purchase.columns = ["user_id", "first_purchase_date"]

print("FIRST PURCHASE SAMPLE")
print(first_purchase.head())

# Create cohort month
first_purchase["cohort_month"] = (
    first_purchase["first_purchase_date"]
    .dt.to_period("M")
)

# Create purchase month
purchases["purchase_month"] = (
    purchases["date"].dt.to_period("M")
)

# Add cohort month to every purchase
purchases = purchases.merge(
    first_purchase[["user_id", "cohort_month"]],
    on="user_id",
    how="left"
)

# Calculate months since first purchase
purchases["months_since_first_purchase"] = (
    (purchases["purchase_month"].dt.year -
    purchases["cohort_month"].dt.year) * 12
    +
    (purchases["purchase_month"].dt.month -
    purchases["cohort_month"].dt.month)
)

print(
    purchases[
        [
            "user_id",
            "purchase_month",
            "cohort_month",
            "months_since_first_purchase"

        ]
    ].head(10)
)

# Count unique purchasing users by cohort and month
cohort_data = (
    purchases
    .groupby(
        ["cohort_month", "months_since_first_purchase"]
    )["user_id"]
    .nunique()
    .reset_index()
)

cohort_data.columns = [
    "cohort_month",
    "months_since_first_purchase",
    "active_users"
]

print("COHORT DATA")
print(cohort_data.head(15))

# Create retention table
retention_table = cohort_data.pivot(
    index = "cohort_month",
    columns = "months_since_first_purchase",
    values = "active_users"
)

print("RETENTION TABLE - USERS")
print(retention_table)

# Convert user counts to retention percent
retention_percentage = (
    retention_table
    .div(retention_table[0], axis = 0)
    * 100
)

print("COHORT RETENTION %")
print(retention_percentage.round(2))

# Save cohort analysis outputs
cohort_data.to_csv(
    "data/cohort_data.csv",
    index=False
)

retention_table.to_csv(
    "data/cohort_retention_users.csv"
)

retention_percentage.round(2).to_csv(
    "data/cohort_retention_percentage.csv"
)

print("Cohort analysis outputs saved successfully.")