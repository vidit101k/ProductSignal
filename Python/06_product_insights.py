import pandas as pd

# Load cleaned data
df = pd.read_csv("data/cleaned_data.csv")

# Normalize funnel columns
funnel_columns = [
    "viewed_product",
    "added_to_cart",
    "checkout_started",
    "purchase_completed"
]

for column in funnel_columns:
    df[column] = (
        df[column]
        .astype(str)
        .str.strip()
        .str.lower()
    )

# Calculate product-view-to-cart conversion
viewed_product_data = df.loc[
    df["viewed_product"].eq("yes")
].copy()

product_view_sessions = len(viewed_product_data)

cart_sessions = (
    viewed_product_data["added_to_cart"].eq("yes").sum()
)

view_to_cart_rate = (
    cart_sessions / product_view_sessions * 100
    if product_view_sessions > 0
    else 0
)

print("PRODUCT INSIGHTS - BASELINE")
print(f"Product-view sessions: {product_view_sessions:,}")
print(f"Sessions adding to cart: {cart_sessions:,}")
print(f"View-to-cart conversion: {view_to_cart_rate:.2f}%")

# Create cart flag
viewed_product_data["cart_flag"] = (
    viewed_product_data["added_to_cart"] == "yes"
)

# Reusable conversion analysis function
def analyze_conversion(data, segment):
    result = data.groupby(segment, dropna=False).agg(
        product_view_sessions = ("cart_flag", "size"),
        cart_sessions = ("cart_flag", "sum")
    )

    result["conversion_rate"] = (
        result["cart_sessions"]
        .div(result["product_view_sessions"])
        .mul(100)
    )    

    result = result.sort_values(
        by = "conversion_rate",
        ascending = False
    )

    return result.round(2)

# Conversion by channel
print("CONVERSION BY CHANNEL")

channel_insights = analyze_conversion(
    viewed_product_data,
    "channel"
)

print(channel_insights)

# Conversion by device
print("CONVERSION BY DEVICE")

device_insights = analyze_conversion(
    viewed_product_data,
    "device"
)

print(device_insights)

# Conversion by user type
print('CONVERSION BY USER TYPE')

user_type_insights = analyze_conversion(
    viewed_product_data,
    "user_type"
)
print(user_type_insights)

# Purchase conversion by channel 

# Create purchase flag
viewed_product_data["purchase_flag"] = (
    viewed_product_data["purchase_completed"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("yes")
)

# Convert revenue to numeric
viewed_product_data["revenue"] = pd.to_numeric(
    viewed_product_data["revenue"],
    errors = "coerce"
).fillna(0)

# Count revenue only from completed purchases
viewed_product_data["purchase_revenue"] = (
    viewed_product_data["revenue"].where(
        viewed_product_data["purchase_flag"],
        0
    )
)

channel_purchase_insights = (
    viewed_product_data.groupby("channel", dropna=False)
    .agg(
        product_view_sessions = ("purchase_flag", "size"),
        purchase_sessions =("purchase_flag", "sum"),
        total_revenue = ("purchase_revenue", "sum")
    )
)

channel_purchase_insights["purchase_conversion_rate"] = (
    channel_purchase_insights["purchase_sessions"]
    / channel_purchase_insights["product_view_sessions"]
    * 100
)

channel_purchase_insights["revenue_per_view_sessions"] = (
    channel_purchase_insights["total_revenue"]
    / channel_purchase_insights["product_view_sessions"]
)

channel_purchase_insights["revenue_per_product_view"] = (
    channel_purchase_insights["total_revenue"]
    / channel_purchase_insights["product_view_sessions"]
)

channel_purchase_insights = channel_purchase_insights.sort_values(
    by = "purchase_conversion_rate",
    ascending = False
).round(2)

print("PURCHASE CONVERSION BY CHANNEL")
print(channel_purchase_insights.round(2))

# Rank channels by revenue per product-view session
channel_efficiency = channel_purchase_insights[
    [
        "product_view_sessions",
        "purchase_sessions",
        "purchase_conversion_rate",
        "total_revenue",
        "revenue_per_product_view"
    ]
].sort_values(
    by = "revenue_per_product_view",
    ascending = False
)

print("CHANNEL REVENUE EFFICIENCY")
print(channel_efficiency.round(2))

# Channel performance interpretation
best_conversion_channel = (
    channel_purchase_insights["purchase_conversion_rate"].idxmax()
)

lowest_conversion_channel = (
    channel_purchase_insights['purchase_conversion_rate'].idxmin()
)

best_revenue_channel = (
    channel_purchase_insights["revenue_per_product_view"].idxmax()
)

lowest_revenue_channel = (
    channel_purchase_insights["revenue_per_product_view"].idxmin()
)

best_revenue_per_view = (
    channel_purchase_insights
    .loc[best_revenue_channel, "revenue_per_product_view"]
)

lowest_revenue_per_view = (
    channel_purchase_insights
    .loc[lowest_revenue_channel, "revenue_per_product_view"]
)

revenue_efficieny_gap = (
    (best_revenue_per_view / lowest_revenue_per_view) - 1
) * 100

print("PRODUCTSIGNAL - CHANNEL INSIGHTS")
print(
    f"Highest purchase conversion: {best_conversion_channel}"
    f"({channel_purchase_insights.loc[best_conversion_channel, 'purchase_conversion_rate']:.2f}%)"
)

print(
    f"Lowest purchase conversion: {lowest_conversion_channel}"
    f"({channel_purchase_insights.loc[lowest_conversion_channel, 'purchase_conversion_rate']:.2f}%)"
)

print(
    f"Highest revenue per product view: {best_revenue_channel}"
    f"({best_revenue_per_view:.2f})"
)

print(
    f"Lowest revenue per product view:"
    f"{lowest_revenue_channel}"
    f"({float(lowest_revenue_per_view):.2f})"
)

print(
    f"Revenue-per-view gap between these channels:"
    f"{revenue_efficieny_gap:.2f}%"
)

# Final product opportunity prioritization

opportunities = pd.DataFrame([
    {
        "opportunity": "Product Page Conversion",
        "business_impact": 5,
        "evidence_strength": 5,
        "implementation_ease": 3,
        "priority_score": 13
    },
    {
        "opportunity": "Checkout Optimization",
        "business_impact": 4,
        "evidence_strength": 4,
        "implementation_ease": 3,
        "priority_score": 11
    },
    {
        "opportunity": "Discount Strategy",
        "business_impact": 4,
        "evidence_strength": 4,
        "implementation_ease": 3,
        "priority_score": 10
    }
])

opportunities = opportunities.sort_values(
    by = "priority_score",
    ascending = False
).reset_index(drop=True)

opportunities.insert(
    0,
    "priority_rank",
    range(1, len(opportunities) + 1)
)

print("PRODUCTSIGNAL - PRODUCT OPPORTUNITY PRIORITIZATION")
print(opportunities.to_string(index=False))

# Save prioritization results
opportunities.to_csv(
    "data/product_opportunity_priorities.csv",
    index=False
)

print("Opportunity prioritization saved successfully.")