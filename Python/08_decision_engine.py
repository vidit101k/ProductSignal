# ProductSignal - Rule-Based Product Decision Engine

from pathlib import Path
import pandas as pd

# Source Dataset
DATA_PATH = Path("data/cleaned_data.csv")
OUTPUT_PATH = Path("data/product_decisions.csv")

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_PATH}."
        "Run this script from the ProductgSignal root folder."
    )

df = pd.read_csv(DATA_PATH)

required_columns = [
    "viewed_product",
    "added_to_cart",
    "purchase_completed",
    "channel",
    "revenue"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Required columns missing from dataset: {missing_columns}"
    )

# Normalize funnel fields
for col in [
    "viewed_product",
    "added_to_cart",
    "purchase_completed"
]:
    df[col] = df[col].astype("string").str.strip().str.lower()

df["revenue"] = pd.to_numeric(
    df["revenue"], errors = "coerce"
).fillna(0)    

# Calculate product-page conversion
product_views = df[df["viewed_product"] == "yes"].copy()

if product_views.empty:
    raise ValueError("No product-view sessions found.")

cart_sessions = (
    product_views["added_to_cart"] == "yes"
).sum()

view_to_cart_rate = (
    cart_sessions / len(product_views) * 100
)

target_view_to_cart_rate = 39.87

# Calculate channel performance
product_views["purchase_flag"] = (
    product_views["purchase_completed"] == "yes"
)

product_views["purchase_revenue"] = (
    product_views["revenue"]
    .where(product_views["purchase_flag"], 0)
)

channel_metrics = (
    product_views.groupby("channel", dropna = False)
    .agg(
        product_view_sessions = ("purchase_flag", "size"),
        purchase_sessions = ("purchase_flag", "sum"),
        total_revenue = ("purchase_revenue", sum)
    )
    .reset_index()
)

channel_metrics["revenue_per_product_view"] = (
    channel_metrics["total_revenue"]
    / channel_metrics["product_view_sessions"]
    * 100
)

channel_metrics = channel_metrics[
    channel_metrics["product_view_sessions"] > 0
]

if channel_metrics.empty:
    raise ValueError("No valid channel metrics could be calculated.")

best_channel_row = channel_metrics.loc[
    channel_metrics["revenue_per_product_view"].idxmax()
]

lowest_channel_row = channel_metrics.loc[
    channel_metrics["revenue_per_product_view"].idxmin()
]

# Generate evidence-based recommendations
decisions = []

if view_to_cart_rate < target_view_to_cart_rate:
    decisions.append({
        "opportunity": "Product Page Conversion",
        "observed_metric": round(view_to_cart_rate, 2),
        "target_scenario": target_view_to_cart_rate,
        "priority": "High",
        "evidence": (
            f"View-to-cart conversion is {view_to_cart_rate:.2f}%,"
            f"compared with the {target_view_to_cart_rate:.2f}%"
            "target scenario."
        ),
        "recommendation": (
            "Investigate product-page friction and run A/B test"
            "before rolling out a change."
        ),
        "validation": "Requires controlled experiment"
    })

decisions.append({
    "opportunity": "Channel Performance",
    "observed_metric": round(
        float(best_channel_row["revenue_per_product_view"]), 2
    ),
    "target_scenario": None,
    "evidence": (
        f"{best_channel_row['channel']} has the highest observed"
        "revenue per product-view session"
        f"(Rs{best_channel_row['revenue_per_product_view']:.2f})."
        f"{lowest_channel_row['channel']} has the lowest"
        f"(Rs{lowest_channel_row['revenue_per_product_view']:.2f})."
    ),
    "recommendation": (
        "Investigate acquisition costs, margins, and incrementality"
        "before changing channel budgets."
    ),
    "validation": "Revenue efficiency is not the same as profitability"
})    

decisions.append({
    "opportunity": "Checkout Optimization",
    "observed_metric": None,
    "target_scenario": None,
    "priority": "Medium",
    "evidence": (
        "Checkout is a proposed product initiative; this engine"
        "does not yet diagnose the cause of checkout drop-off."
    ),
    "recommendation": (
        "Review checkout-stage metric and user friction before"
        "selecting a change to test."
    ),
    "validation": "Requires further investigation"
})

# Save and display recommendations
decision_table = pd.DataFrame(decisions)

priority_order = {
    "High": 1,
    "Medium": 2,
    "Low": 3
}

decision_table["_sort_order"] = (
    decision_table["priority"].map(priority_order)
)

decision_table = (
    decision_table
    .sort_values("_sort_order")
    .drop(columns = "_sort_order")
    .reset_index(drop = True)
)

OUTPUT_PATH.parent.mkdir(parents = True, exist_ok = True)
decision_table.to_csv(OUTPUT_PATH, index = False)

print("PRODUCTSIGNAL - DATA-DRIVEN DECISION ENGINE")
print("-" * 55)
print(f"Dataset rows loaded: {len(df):,}")
print(f"Product-view sessions: {len(product_views):,}")
print(f"View-to-cart conversion: {view_to_cart_rate:.2f}%")

print("CHANNEL PERFORMANCE")
print(
    channel_metrics.sort_values(
        "revenue_per_product_view",
        ascending = False 
    ).to_string(index = False)
)

print("PRODUCT DECISIONS")
for index, decision in decision_table.iterrows():
    print(f"{index + 1}, {decision['opportunity']}")
    print(f"Priority: {decision['priority']}")
    print(f"Evidence: {decision['evidence']}")
    print(f"Recommendation: {decision['recommendation']}")
    print(f"Validation: {decision['validation']}")

print(f"Decision report saved to: {OUTPUT_PATH}")
print("Note: Results describe synthetic educational data.")   

