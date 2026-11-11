import pandas as pd

# Load cleaned data
df = pd.read_csv("data/cleaned_data.csv")

# Convert date
df["date"] = pd.to_datetime(df["date"])

# Normalize purchase column
df["purchase_completed"] = (
    df["purchase_completed"]
    .astype(str)
    .str.strip()
    .str.lower()
)

# Keep completed purchases
purchases = df[df["purchase_completed"] == "yes"].copy()

print("Purchase sessions:", len(purchases))
print("Unique purchasing users:", purchases["user_id"].nunique())

# Core financial metrics
total_revenue = purchases["revenue"].sum()
total_orders = len(purchases)
unique_customers = purchases["user_id"].nunique()

aov = total_revenue / total_orders
revenue_per_customer = total_revenue / unique_customers

print("PRODUCTSIGNAL FINANCIAL KPIs")
print(f"Total Revenue: {total_revenue:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Unique Customers: {unique_customers:,}")
print(f"Average Order Values: {aov:,.2f}")
print(f"Average per Customer: {revenue_per_customer:,.2f}")

# Revenue by channel
channel_revenue = (
    purchases.groupby("channel")
    .agg(
        orders = ("session_id", "count"),
        revenue = ("revenue", "sum")
    )
)

channel_revenue["aov"] = (
    channel_revenue["revenue"]
    / channel_revenue["orders"]
)

print("REVENUE BY CHANNEL")
print(channel_revenue.sort_values("revenue", ascending = False))

channel_revenue["revenue_share"] = (
    channel_revenue["revenue"]
    / total_revenue
    * 100
)

print("CHANNEL REVENUE CONTRIBUTION")
print(
    channel_revenue
    .sort_values("revenue", ascending = False)
    .round(2)
)

# Revenue by device
device_revenue = (
    purchases.groupby("device")
    .agg(
        orders = ("session_id", "count"),
        revenue = ("revenue", "sum")
    )
)

device_revenue["aov"] = (
    device_revenue["revenue"]
    / device_revenue["orders"]
)

device_revenue["revenue_share"] = (
    device_revenue["revenue"]
    / total_revenue
    * 100
)

print("REVENUE BY DEVICE")
print(
    device_revenue
    .sort_values("revenue", ascending = False)
    .round(2)
)

# Revenue by discount
discount_revenue = ( 
    purchases.groupby("discount_applied")
    .agg(
        orders = ("session_id", "count"),
        revenue = ("revenue", "sum")
    )
)

discount_revenue["aov"] = (
    discount_revenue["revenue"]
    / discount_revenue["orders"]
)

discount_revenue["revenue_share"] = (
    discount_revenue["revenue"]
    / total_revenue
    * 100
)

print("REVENUE BY DISCOUNT")
print(
    discount_revenue
    .sort_values("revenue", ascending = False)
    .round(2)
)

# Sequential Funnel Counts
visited = (
    df["visited_website"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("yes")
)

viewed = (
    df["viewed_product"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("yes")
)

carted = (
    df["added_to_cart"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("yes")   
)

checkout_started = (
    df["checkout_started"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("yes")
)

purchased_flag = (
    df["purchase_completed"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("yes")
)

# Sequential stages
website_visits = visited.sum()

product_views = (
    visited & viewed
).sum()

add_to_cart = (
    visited & viewed & carted
).sum()

checkout = (
    visited & viewed & carted & checkout_started
).sum()

purchase_count = (
    visited & carted & checkout_started & purchased_flag
).sum()

print("SEQUENTIAL FUNNEL")
print(f"Website Visits: {website_visits:,}")
print(f"Product Views: {product_views:,}")
print(f"Add to Cart: {add_to_cart:,}")
print(f"Checkout Started: {checkout:,}")
print(f"Purchases: {purchase_count:,}")

# Sequential conversion rates
product_view_rate = (
    product_views / website_visits * 100
)

cart_rate = (
    add_to_cart / product_views * 100
)

checkout_rate = (
    checkout / add_to_cart * 100
)

purchase_rate = (
    purchase_count / checkout * 100
)

overall_conversion = (
    purchase_count / website_visits * 100 
)

print("SEQUENTIAL CONVERSION RATES")
print(f"Visit to Product View: {product_view_rate:.2f}%")
print(f"Product View - Add to Cart: {cart_rate:.2f}%")
print(f"Add to Cart - Checkout: {cart_rate:.2f}%")
print(f"Checkout - Purchase: {checkout_rate:.2f}%")
print(f"Overall Visit - Purchase: {overall_conversion:.2f}%")

# Opportunity Sizing
current_cart_rate = add_to_cart / product_views

# Assuming we improve the cart conversion rate by 5 percentage points
target_cart_rate = current_cart_rate + 0.05

# Additional customers who would add to cart
additional_carts = (
    product_views
    * (target_cart_rate - current_cart_rate)
)

# Current downstream conversion rates
cart_to_checkout_rate = checkout / add_to_cart

checkout_to_purchase_rate = purchase_count / checkout

# Additional checkouts generated
additional_checkouts = (
    additional_carts
    * cart_to_checkout_rate
)

# Additional purchase generated
additional_purchases = (
    additional_carts
    * checkout_to_purchase_rate
)

# Incremental revenue
incremental_revenue = (
    additional_purchases
    * aov
)

print("OPPORTUNITY SIZING")
print(f"Current Product View - Cart Rate: {current_cart_rate * 100:.2f}%")
print(f"Target Product View - Cart Rate : {target_cart_rate * 100:.2f}%")
print(f"Additional Carts: {additional_carts:,.0f}")
print(f"Additional Checkouts: {additional_checkouts:,.0f}")
print(f"Additional Purchases: {additional_purchases:,.0f}")
print(f"Estimated Incremental Revenue : {incremental_revenue:,.2f}")

# Incremental profit analysis

# Assumption for the business scenario
contribution_margin = 0.20
improvement_cost = 200000

# Calaculate incremental contribution
incremental_contribution = (
    incremental_revenue * contribution_margin
)

# Calculate contribution after improvement cost
net_incremental_profit = (
    incremental_contribution - improvement_cost
)

print(f"Incremental Revenue: {incremental_revenue:,.2f}")
print(f"Assumed Contribution Margin: {contribution_margin:.0f}")
print(f"Incremental Contribution: {incremental_contribution:,.2f}")
print(f"Improvement Cost: {improvement_cost:,.2f}")
print(f"Net Incremental Contribution: {net_incremental_profit:,.2f}")

# ROI analysis
roi = (
    net_incremental_profit / improvement_cost
) * 100

print("ROI ANALYSIS")
print(f"Estimated ROI: {roi:.2f}%")

# OPPORTUNITY PRIOTIZATION
opportunities = pd.DataFrame({
    "opportunity": [
        "Improve Product Page Conversion",
        "Optimize Checkout Experience",
        "Review Discount Strategy"
    ],
    "potential_impact" : [
        "High",
        "High",
        "Medium"
    ],
    "implementation_effort": [
        "Medium",
        "Medium",
        "Medium"
    ],
    "priority":[
        1,
        2,3
    ]
})

opportunities = opportunities.sort_values("priority")

print("OPPORTUNITY PRIORITIZATION")
print(opportunities.to_string(index=False))