import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from ai_insights import generate_ai_response

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ProductSignal | Decision Center",
    page_icon="📊",
    layout="wide"
)

YES = "yes"

# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

DATA_PATH = (
    Path(__file__).resolve().parent
    / "data"
    / "cleaned_data.csv"
)


@st.cache_data
def load_data(path):
    df = pd.read_csv(path)

    df.columns = df.columns.str.strip()

    # Normalize categorical flags
    flag_columns = [
        "visited_website",
        "viewed_product",
        "added_to_cart",
        "checkout_started",
        "purchase_completed",
        "discount_applied",
    ]

    for column in flag_columns:
        if column in df.columns:
            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
                .str.lower()
            )

    df["date"] = pd.to_datetime(
        df["date"], errors="coerce"
    )

    for column in ["order_value", "revenue"]:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    return df


st.title("📊 ProductSignal")
st.caption(
    "Product Growth & Decision Intelligence System"
)

if not DATA_PATH.exists():
    st.error(
        "Dataset not found. Ensure cleaned_data.csv "
        "is inside the project's data folder."
    )
    st.code("ProductSignal/data/cleaned_data.csv")
    st.stop()

df = load_data(str(DATA_PATH))

required_columns = [
    "date",
    "channel",
    "device",
    "user_type",
    "viewed_product",
    "added_to_cart",
    "checkout_started",
    "purchase_completed",
    "discount_applied",
    "order_value",
    "revenue",
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        "Required columns are missing: "
        + ", ".join(missing_columns)
    )
    st.stop()

if df.empty:
    st.warning("The dataset contains no rows.")
    st.stop()

# --------------------------------------------------
# 3. SIDEBAR NAVIGATION AND FILTERS
# --------------------------------------------------

st.sidebar.title("ProductSignal")
st.sidebar.caption("Decision Center")

page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Funnel Analysis",
        "Channel Performance",
        "Customer Insights",
        "Decision Center",
        "A/B Testing",
        "AI Insights"
    ],
)

st.sidebar.divider()
st.sidebar.subheader("Interactive Filters")

channels = sorted(
    df["channel"].dropna().unique().tolist()
)

devices = sorted(
    df["device"].dropna().unique().tolist()
)

selected_channels = st.sidebar.multiselect(
    "Marketing channels",
    options=channels,
    default=channels,
)

selected_devices = st.sidebar.multiselect(
    "Devices",
    options=devices,
    default=devices,
)

valid_dates = df["date"].dropna()

if valid_dates.empty:
    min_date = None
    max_date = None
else:
    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

if min_date is not None and max_date is not None:
    date_range = st.sidebar.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
else:
    date_range = None

filtered = df.copy()

filtered = filtered[
    filtered["channel"].isin(selected_channels)
    & filtered["device"].isin(selected_devices)
]

if date_range is not None:
    if isinstance(date_range, (tuple, list)):
        if len(date_range) == 2:
            start_date, end_date = date_range

            filtered = filtered[
                filtered["date"].dt.date.between(
                    start_date, end_date
                )
            ]
        elif len(date_range) == 1:
            selected_date = date_range[0]

            filtered = filtered[
                filtered["date"].dt.date == selected_date
            ]
    else:
        filtered = filtered[
            filtered["date"].dt.date == date_range
        ]

if filtered.empty:
    st.warning(
        "No records match these filters. "
        "Select more channels, devices, or dates."
    )
    st.stop()

# --------------------------------------------------
# 4. METRICS
# --------------------------------------------------

# Financial KPIs:
# Use all rows flagged as completed purchases.
# This matches the original purchase-flag definition.

completed_purchases = filtered[
    filtered["purchase_completed"] == YES
]

total_revenue = completed_purchases[
    "revenue"
].fillna(0).sum()

total_orders = len(completed_purchases)

aov = (
    total_revenue / total_orders 
    if total_orders > 0
    else 0
)

unique_customers = (
    completed_purchases["user_id"].nunique()
    if "user_id" in completed_purchases.columns
    else 0
)

# Sequential funnel:
# Each stage is measured only among users/sessions
# that reached the preceding stage.

product_views = filtered[
    filtered["viewed_product"] == YES
]

cart_rows = product_views[
    product_views["added_to_cart"] == YES
]

checkout_rows = cart_rows[
    cart_rows["checkout_started"] == YES
]

funnel_purchases = checkout_rows[
    checkout_rows["purchase_completed"] == YES
]

view_count = len(product_views)
cart_count = len(cart_rows)
checkout_count = len(checkout_rows)
funnel_purchase_count = len(funnel_purchases)

view_to_cart = (
    cart_count / view_count * 100
    if view_count else 0
)

cart_to_checkout = (
    checkout_count / cart_count * 100
    if cart_count else 0
)

checkout_to_purchase = (
    funnel_purchase_count / checkout_count * 100
    if checkout_count else 0
)

overall_conversion = (
    total_orders / len(filtered) * 100
    if len(filtered) else 0
)

# --------------------------------------------------
# 5. HELPER FUNCTIONS
# --------------------------------------------------

def show_metric_row():
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Revenue",
        f"₹{total_revenue:,.2f}"
    )

    col2.metric(
        "Completed Orders",
        f"{total_orders:,}"
    )

    col3.metric(
        "Average Order Value",
        f"₹{aov:,.2f}"
    )

    col4.metric(
        "Unique Customers",
        f"{unique_customers:,}"
    )


def style_chart(fig):
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=55, b=20),
        legend_title_text="",
    )
    return fig


# --------------------------------------------------
# 6. OVERVIEW
# --------------------------------------------------

if page == "Overview":

    st.header("Business Overview")
    st.write(
        "Monitor revenue, orders, conversion, "
        "and the overall customer journey."
    )

    show_metric_row()

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Revenue by Channel")

        revenue_by_channel = (
            completed_purchases
            .groupby("channel", dropna=False)["revenue"]
            .sum()
            .reset_index()
            .sort_values("revenue", ascending=False)
        )

        if not revenue_by_channel.empty:
            fig = px.bar(
                revenue_by_channel,
                x="channel",
                y="revenue",
                title="Completed-Purchase Revenue",
                labels={
                    "channel": "Channel",
                    "revenue": "Revenue (₹)",
                },
            )
            st.plotly_chart(
                style_chart(fig),
                use_container_width=True,
            )
        else:
            st.info("No revenue data available.")

    with right:
        st.subheader("Customer Device Distribution")

        device_counts = (
            filtered["device"]
            .value_counts()
            .rename_axis("device")
            .reset_index(name="sessions")
        )

        if not device_counts.empty:
            fig = px.pie(
                device_counts,
                names="device",
                values="sessions",
                title="Sessions by Device",
                hole=0.45,
            )
            st.plotly_chart(
                style_chart(fig),
                use_container_width=True,
            )
        else:
            st.info("No device data available.")

    st.divider()
    st.subheader("Funnel Snapshot")

    f1, f2, f3, f4 = st.columns(4)

    f1.metric("Product Views", f"{view_count:,}")
    f2.metric("Added to Cart", f"{cart_count:,}")
    f3.metric("Checkout Started", f"{checkout_count:,}")
    f4.metric("Sequential Purchases", f"{funnel_purchase_count:,}")

    st.caption(
        "Financial KPIs use the dataset's completed-purchase flag. "
        "Funnel counts use sequential stage filtering. "
        "These counts can differ because the source flags are not "
        "perfectly consistent."
    )

# --------------------------------------------------
# 7. FUNNEL ANALYSIS
# --------------------------------------------------

elif page == "Funnel Analysis":

    st.header("Conversion Funnel")
    st.write(
        "Explore progression through product views, "
        "cart additions, checkout, and purchase."
    )

    stages = pd.DataFrame({
        "Stage": [
            "Product Views",
            "Added to Cart",
            "Checkout Started",
            "Completed Purchases",
        ],
        "Sessions": [
            view_count,
            cart_count,
            checkout_count,
            funnel_purchase_count,
        ],
    })

    fig = px.funnel(
        stages,
        x="Sessions",
        y="Stage",
        title="Sequential Conversion Funnel",
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True,
    )

    st.subheader("Stage Conversion Rates")

    r1, r2, r3 = st.columns(3)

    r1.metric(
        "View → Cart",
        f"{view_to_cart:.2f}%"
    )

    r2.metric(
        "Cart → Checkout",
        f"{cart_to_checkout:.2f}%"
    )

    r3.metric(
        "Checkout → Purchase",
        f"{checkout_to_purchase:.2f}%"
    )

    st.info(
        f"The largest measurable drop-off starts with "
        f"{view_count - cart_count:,} sessions between product "
        f"views and cart additions. Investigate product-page "
        f"clarity, pricing, trust signals, and calls to action "
        f"before deciding on an experiment."
    )

    st.caption(
        "These are sequential counts derived from the available "
        "session flags. Validate event definitions before using "
        "them as production conversion metrics."
    )

# --------------------------------------------------
# 8. CHANNEL PERFORMANCE
# --------------------------------------------------

elif page == "Channel Performance":

    st.header("Channel Performance")
    st.write(
        "Compare marketing channels using completed-purchase "
        "revenue, order count, average order value, and "
        "product-view conversion."
    )

    channel_summary = (
        product_views
        .groupby("channel", dropna = False)
        .size()
        .reset_index(name = "Product Views")
    )

    financial_summary = (
        completed_purchases
        .groupby("channel", dropna = False)
        .agg(
            Revenue = ("revenue", "sum"),
            Orders = ("purchase_completed", "size"),
            AOV = ("order_value", "mean"),
    )
    .reset_index()
)

    view_purchase_summary = (
        product_views[
            product_views["purchase_completed"] == YES
    ]
    .groupby("channel", dropna = False)
    .size()
    .reset_index(name = "Purchases After Product View")
)

    channel_summary = (
        channel_summary
        .merge(financial_summary, on = "channel", how = "left")
        .merge(view_purchase_summary, on = "channel", how = "left")
)

    channel_summary["Revenue"] =channel_summary["Revenue"].fillna(0)
    channel_summary["Orders"] = channel_summary["Orders"].fillna(0)
    channel_summary["Purchases After Product View"] = (
        channel_summary["Purchases After Product View"].fillna(0)
)

    channel_summary["View-to-Purchase Rate (%)"] = (
        channel_summary["Purchases After Product View"]
        / channel_summary["Product Views"].replace(0, pd.NA)
        * 100
).fillna(0)

    channel_summary = channel_summary.sort_values(
        "Revenue", ascending = False
)


    channel_summary = channel_summary.sort_values(
        "Revenue",
        ascending=False,
    )

    st.dataframe(
        channel_summary.round(2),
        use_container_width=True,
        hide_index=True,
    )

    left, right = st.columns(2)

    with left:
        fig = px.bar(
            channel_summary,
            x="channel",
            y="Revenue",
            title="Revenue by Channel",
            labels={
                "channel": "Channel",
                "Revenue": "Revenue (₹)",
            },
        )
        st.plotly_chart(
            style_chart(fig),
            use_container_width=True,
        )

    with right:
        fig = px.bar(
            channel_summary,
            x="channel",
            y="View-to-Purchase Rate (%)",
            title="Product View to Purchase Rate",
            labels={
                "channel": "Channel",
                "View-to-Purchase Rate (%)": "Rate (%)",
            },
        )
        st.plotly_chart(
            style_chart(fig),
            use_container_width=True,
        )

    st.caption(
        "Revenue and order metrics use the completed-purchase flag. "
        "The view-to-purchase rate uses purchase-flagged rows among "
        "product-view rows. These are different definitions."
    )

# --------------------------------------------------
# 9. CUSTOMER INSIGHTS
# --------------------------------------------------

elif page == "Customer Insights":

    st.header("Customer Insights")
    st.write(
        "Compare new and returning users and examine "
        "device-level cart-addition behavior."
    )

    left, right = st.columns(2)

    with left:
        st.subheader("New vs Returning Users")

        user_summary = (
            filtered
            .groupby("user_type", dropna=False)
            .agg(
                Sessions=("session_id", "nunique")
                if "session_id" in filtered.columns
                else ("user_type", "size"),
                Users=("user_id", "nunique")
                if "user_id" in filtered.columns
                else ("user_type", "size"),
            )
            .reset_index()
        )

        fig = px.bar(
            user_summary,
            x="user_type",
            y="Sessions",
            title="Sessions by User Type",
            labels={
                "user_type": "User Type",
                "Sessions": "Sessions",
            },
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True,
        )

        st.dataframe(
            user_summary,
            use_container_width=True,
            hide_index=True,
        )

    with right:
        st.subheader("View-to-Cart Rate by Device")

        device_views = (
            product_views
            .groupby("device", dropna=False)
            .size()
            .reset_index(name="Product Views")
        )

        device_carts = (
            cart_rows
            .groupby("device", dropna=False)
            .size()
            .reset_index(name="Added to Cart")
        )

        device_summary = device_views.merge(
            device_carts,
            on="device",
            how="left",
        )

        device_summary["Added to Cart"] = (
            device_summary["Added to Cart"].fillna(0)
        )

        device_summary["View-to-Cart Rate (%)"] = (
            device_summary["Added to Cart"]
            / device_summary["Product Views"].replace(0, pd.NA)
            * 100
        ).fillna(0)

        fig = px.bar(
            device_summary,
            x="device",
            y="View-to-Cart Rate (%)",
            title="Product View to Cart Rate by Device",
            labels={
                "device": "Device",
                "View-to-Cart Rate (%)": "Rate (%)",
            },
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True,
        )

        st.dataframe(
            device_summary.round(2),
            use_container_width=True,
            hide_index=True,
        )

# --------------------------------------------------
# 10. DECISION CENTER
# --------------------------------------------------

elif page == "Decision Center":
    st.title("Decision Center")
    st.caption(
        "Prioritized business opportunities based on ProductSignal's"
        "synthetic e-commerce dataset."
    )

    decisions_path = Path("data/product_decisions.csv")

    if not decisions_path.exists():
        st.warning(
            "Decision file not found. Run 08_decision.py first."
        )
    else:
        decisions = pd.read_csv(decisions_path)

        required_columns = [
            "opportunity",
            "evidence",
            "recommendation",
            "priority",
            "validation",
        ]

        if not all(
            column in decisions.columns
            for column in required_columns
        ):
            st.error(
                "The decision CSV is missing one or more required columns."
            )
        else:
            priority_order = {
                "High": 0,
                "Medium": 1,
                "Low": 2,
            }

            decisions["_priority_order"] = (
                decisions["priority"]
                .map(priority_order)
                .fillna(3)
            )

            decisions = decisions.sort_values("_priority_order")

            st.subheader("Prioritized Opportunities")

            for _, decision in decisions.iterrows():
                with st.container(border = True):
                    st.subheader(decision["opportunity"])

                    st.caption(
                        f"Priority: {decision['priority']}"
                    )

                    st.markdown("**Evidence**")
                    st.write(decision["evidence"])

                    st.markdown("**Recommended action**")
                    st.write(decision["recommendation"])

                    st.markdown("**Validation required**")
                    st.write(decision["validation"]) 

            st.caption(
                "Recommendations are based on synthetic portfolio data "
                "and should be validated before business decisions."
            )     

# --------------------------------------------------
# 11. A/B TESTING
# --------------------------------------------------

elif page == "A/B Testing":
    st.title("A/B Testing")
    st.caption("Experiment analysis | Simulated practice data")

    from pathlib import Path
    import pandas as pd

    project_root = Path(__file__).resolve().parent
    results_file = project_root / "data" / "ab_testing.csv"

    if not results_file.exists():
        st.warning(
            "A/B test results not found."
            "Run python/07_ab_testing.py first."
        )
    else:
        results = pd.read_csv(results_file)

        # Noramlize CSV column names
        results.columns =(
            results.columns
            .str.strip()
            .str.replace(r"\s+", "_", regex = True)
        )

        if results.empty:
            st.warning("The A/B testing results file is empty.")
        else:
            result = results.iloc[0]

            st.info(
                "These are simulated practice results, "
                "not outcomes from a live experiment."
            )

            control_rate = float(result["control_conversion_rate"])
            variant_rate = float(result["variant_conversion_rate"])
            absolute_lift = float(result["absolute_lift"])
            relative_lift = float(result["relative_lift"])
            p_value = float(result["p_value"])

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Control Conversion",
                f"{control_rate:.2%}"
            )
            col2.metric(
                "Variant_Conversion",
                f"{variant_rate:.2%}",
                delta = f"{absolute_lift * 100:.2f} percentage points"
            )
            col3.metric(
                "Relative Conversion Lift",
                f"{relative_lift:.2%}"
            )

            st.subheader("Experiment Results")

            col1, col2 = st.columns(2)

            col1.metric("P-value", f"{p_value:.6g}")

            significant = bool(result["statistically_significant"])
            col2.metric(
                "Statistical Significance",
                "Significant" if significant else "Not significant"
            )        

            st.subheader("95% Confidence Interval")

            ci_lower = float(result["ci_lower"])
            ci_upper = float(result["ci_upper"])

            st.write(
                f"Conversion-rate difference: "
                f"{ci_lower * 100:.2f} to {ci_upper * 100:.2f} "
                f"percentage points"
            )

            st.subheader("Revenue Guardrail")

            control_rpv = float(
                result["control_revenue_per_visitor"]
            )
            variant_rpv = float(
                result["variant_revenue_per_visitor"]
            )
            revenue_change = float(result["revenue_change"])

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Control Revenue / Visitor",
                f"₹{control_rpv:.2f}"
            )

            col2.metric(
                "Variant Revenue / Visitor",
                f"₹{variant_rpv:.2f}"
            )
            col3.metric(
                "Revenue Change",
                f"{revenue_change:.2%}"
            )

            guardrail_passed = bool(
                result["revenue_guardrail_passed"]
            )

            if guardrail_passed:
                st.success("Revenue guardrail passed.")
            else:
                st.error("Revenue guardrail failed.")

            st.subheader("Final Decision")

            decision = str(result["decision"])
            st.write(decision)        


# --------------------------------------------------
# 12. AI INSIGHTS
# --------------------------------------------------

elif page == "AI Insights":

    st.title("AI Business Insights")
    st.caption(
        "AI-powered interpretation of ProductSignal's "
        "filtered business metrics."
    )

    st.write(
        "Generate business insights and recommendations "
        "using the data selected in the sidebar filters."
    )

    # Calculate aggregate business metrics
    total_revenue = completed_purchases["revenue"].sum()
    total_orders = len(completed_purchases)

    average_order_value = (
        completed_purchases["order_value"].mean()
        if total_orders > 0
        else 0
    )

    total_views = len(product_views)
    total_carts = len(cart_rows)

    view_cart_rate = (
        total_carts / total_views * 100
        if total_views > 0
        else 0
    )

    # Additional funnel metrics
    cart_to_checkout_rate = (
        checkout_count / cart_count * 100
        if cart_count > 0
        else 0
    )

    checkout_to_purchase_rate = (
        funnel_purchase_count / checkout_count * 100
        if checkout_count > 0
        else 0
    )

    net_revenue_per_order = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )

    # Repeat customer analysis
    customer_orders = (
        completed_purchases
        .groupby("user_id")
        .size()
    )

    repeat_customers = int((customer_orders > 1).sum())
    one_time_customers = int((customer_orders == 1).sum())

    # Monthly revenue analysis
    monthly_revenue = (
        completed_purchases
        .assign(month=completed_purchases["date"].dt.to_period("M"))
        .groupby("month")["revenue"]
        .sum()
    )

    monthly_data = (
        monthly_revenue.round(2).to_string()
        if not monthly_revenue.empty
        else "No monthly revenue data available."
    )


    # Channel-level revenue summary
    if not completed_purchases.empty:
        channel_summary_ai = (
            completed_purchases
            .groupby("channel", dropna=False)
            .agg(
                Revenue=("revenue", "sum"),
                Orders=("purchase_completed", "size"),
            )
            .reset_index()
            .sort_values("Revenue", ascending=False)
        )

        channel_data = channel_summary_ai.round(2).to_string(
            index=False
        )
    else:
        channel_data = "No completed purchases in the selected data."

    st.subheader("Current Filtered Business Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Revenue", f"₹{total_revenue:,.2f}")
    col2.metric("Completed Orders", f"{total_orders:,}")
    col3.metric("Average Order Value", f"₹{average_order_value:,.2f}")

    col1, col2, col3 = st.columns(3)

    col1.metric("Product Views", f"{total_views:,}")
    col2.metric("Added to Cart", f"{total_carts:,}")
    col3.metric("View-to-Cart Rate", f"{view_cart_rate:.2f}%")

    st.divider()

    st.subheader("Ask ProductSignal AI")

    user_question = st.text_area(
        "What would you like to understand?",
        placeholder=(
            "Example: What is the biggest business opportunity "
            "in the current data?"
        ),
    )

    if st.button("Generate AI Insights", type="primary"):

        
        prompt = f"""
You are a product analytics and business strategy assistant
for an e-commerce product called ProductSignal.

Analyze the following aggregate business data.

OVERALL BUSINESS PERFORMANCE:
- Net revenue: ₹{total_revenue:.2f}
- Completed orders: {total_orders}
- Gross average order value: ₹{average_order_value:.2f}
- Net revenue per order: ₹{net_revenue_per_order:.2f}

FUNNEL PERFORMANCE:
- Product views: {total_views}
- Added to cart: {total_carts}
- Checkout started: {checkout_count}
- Sequential purchases: {funnel_purchase_count}
- View-to-cart rate: {view_cart_rate:.2f}%
- Cart-to-checkout rate: {cart_to_checkout_rate:.2f}%
- Checkout-to-purchase rate: {checkout_to_purchase_rate:.2f}%

CUSTOMER PERFORMANCE:
- One-time customers: {one_time_customers}
- Repeat customers: {repeat_customers}

CHANNEL PERFORMANCE:
{channel_data}

MONTHLY REVENUE:
{monthly_data}

USER QUESTION:
{user_question if user_question.strip() else "Generate an executive business sales report."}

ANALYSIS INSTRUCTIONS:

1. Identify the most important business findings.
2. Identify the biggest measurable business opportunity.
3. Explain funnel performance and where the largest drop-off occurs.
4. Evaluate channel performance using the supplied metrics.
5. Give practical product and business recommendations.
6. Suggest relevant KPIs to monitor.
7. Explain expected business impact without inventing numerical estimates.

IMPORTANT RULES:

- Use only the supplied data for factual claims.
- Clearly distinguish:
  FACT: Directly supported by supplied data.
  HYPOTHESIS: A possible explanation that needs validation.
  RECOMMENDATION: A proposed action based on the evidence.
- Never present a hypothesis as a proven cause.
- Do not invent CAC, LTV, profit margins, advertising costs,
  or marketing ROI.
- Do not claim that a channel is profitable without cost data.
- Do not claim that an intervention will increase conversion
  without experiment evidence.
- If information is unavailable, explicitly say so.
- Distinguish gross AOV from net revenue per order.
- Keep the report professional, structured and concise.

This is a synthetic portfolio dataset, not verified
real-world business performance.
"""

        try:
            with st.spinner("ProductSignal AI is analyzing the data..."):

                ai_response = generate_ai_response(prompt)

            st.subheader("AI Analysis")
            st.markdown(ai_response)

        except Exception as e:
            st.error(
                "Unable to generate AI insights. "
                "Please try again later."
            )
            st.caption(f"Technical details: {e}")


# --------------------------------------------------
# 13. FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "ProductSignal | Portfolio project using synthetic "
    "e-commerce data. Findings are illustrative and should "
    "not be represented as results from a real company."
)