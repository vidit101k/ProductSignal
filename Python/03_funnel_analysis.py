import pandas as pd

# Load cleaned data
df = pd.read_csv("data/cleaned_data.csv")
print(df["visited_website"].value_counts(dropna=False))
print(df["visited_website"].unique())
print(df.dtypes)

# Total sessions
total_sessions = len(df)

# Funnel counts
website_visits = (df["visited_website"].str.lower() == "yes").sum()
product_views = (df["viewed_product"].str.lower() == "yes").sum()
add_to_cart = (df["added_to_cart"].str.lower() == "yes").sum()
checkout = (df["checkout_started"].str.lower() == "yes").sum()
purchases = (df["purchase_completed"].str.lower() == "yes").sum()

# Conversion rates
print("FUNNEL COUNTS")

print("Website visits:", website_visits)
print("Product views:", product_views)
print("Add to cart:", add_to_cart)
print("Checkout started:", checkout)
print("Purchases:", purchases)

print("UNIQUE FUNNNEL VALUES")

for column in [
    "visited_website",
    "viewed_product",   
    "added_to_cart",
    "checkout_started",
    "purchase_completed"
]:
    print(f"{column}")
    print(df[column].value_counts(dropna=False))

# Safe conversion calculations
def conversion_rate(numerator, denominator):
    if denominator == 0:
        return 0
    return numerator / denominator * 100

product_view_rate = conversion_rate(product_views, website_visits)
cart_rate = conversion_rate(add_to_cart, product_views)
checkout_rate = conversion_rate(checkout, add_to_cart)
purchase_rate = conversion_rate(purchases, checkout)
overall_conversion = conversion_rate(purchases, website_visits)

# Funnel Bottleneck Analysis
print("BOTTLENECK ANALYSIS")
print(df.columns.tolist())

# Bottlneck Analysis: Channel
print("ADD TO CART RATE BY CHANNEL")

channel_analysis = (
    df[df["viewed_product"].str.lower() == "yes"]
    .groupby("channel")["added_to_cart"]
    .apply(lambda x:(x.str.lower() == "yes").mean() * 100)
    .sort_values()
)

print(channel_analysis)

# Bottleneck Analysis: Device
print("ADD TO CART RATE BY DEVICE")

device_analysis = (
    df[df["viewed_product"].str.lower() == "yes"]
    .groupby("device")["added_to_cart"]
    .apply(lambda x:(x.str.lower() == "yes").mean() * 100)
    .sort_values()
)

print(device_analysis)

# Bottleneck Analysis: User Type
print("ADD TO CART RATE BY USER TYPE")

user_type_analysis = (
    df[df["viewed_product"].str.lower() == "yes"]
    .groupby("user_type")["added_to_cart"]
    .apply(lambda x:(x.str.lower() == "yes").mean() * 100)
    .sort_values()
)

print(user_type_analysis)

# Bottleneck Analysis: Region
print("ADD TO CART RATE BY REGION")

region_analysis = (
    df[df["viewed_product"].str.lower() == "yes"]
    .groupby("region")["added_to_cart"]
    .apply(lambda x:(x.str.lower() == "yes").mean() * 100)
    .sort_values()
)

print(region_analysis)

# Bottlneck Analysis: Discount
print("ADD TO CART RATE BY DISCOUNT")

discount_analysis = (
    df[df["viewed_product"].str.lower() == "yes"]
    .groupby("discount_applied")["added_to_cart"]
    .apply(lambda x:(x.str.lower() == "yes").mean() * 100)
    .sort_values()
)

print(discount_analysis)

# Bottleneck Analysis: Discount vs Add to Cart
print("DISCOUNT VS ADD TO CART")

discount_cart_table = pd.crosstab(
    df["discount_applied"],
    df["added_to_cart"],
    normalize = "index"
) * 100

print(discount_cart_table)

print("PRODUCTSIGNAL FUNNEL")

print("Website visits:", website_visits)
print("Product views:", product_views)
print("Add to cart:", add_to_cart)
print("Checkout started:", checkout)
print("Purchases :", purchases)

print(f"Visit to Product View: {product_view_rate:.2f}%")
print(f"Product View to Cart: {cart_rate:.2f}%")
print(f"Cart to Checkout: {checkout_rate:.2f}%")
print(f"Checkout to Purchase: {purchase_rate:.2f}%")
print(f"Overall Conversion: {overall_conversion:.2f}%") 