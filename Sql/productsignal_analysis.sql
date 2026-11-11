-- ==================================================
-- PROJECT: ProductSignal
-- MODULE: SQL Analytics
-- DATABASE: productsignal
-- DATASET: 120,000 Records
-- PURPOSE: Product, Customer & Business Analysis
-- ==================================================


-- ==================================================
-- SECTION 01: DATABASE SETUP & DATA VALIDATION
-- ==================================================

USE productsignal;


-- Query 1: Total records

SELECT COUNT(*) AS total_records
FROM product_data;


-- Query 2: Unique customers

SELECT COUNT(DISTINCT user_id) AS unique_customers
FROM product_data;


-- Query 3: Check duplicate sessions

SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT session_id) AS unique_sessions
FROM product_data;


-- Query 4: Check missing values

SELECT
    SUM(user_id IS NULL) AS missing_user_ids,
    SUM(session_id IS NULL) AS missing_sessions,
    SUM(date IS NULL) AS missing_dates,
    SUM(revenue IS NULL) AS missing_revenue
FROM product_data;


-- Query 5: Check purchase records

SELECT
    purchase_completed,
    COUNT(*) AS total_records
FROM product_data
GROUP BY purchase_completed;


-- ==================================================
-- SECTION 02: OVERALL BUSINESS KPIs
-- ==================================================

-- Query 1: Overall business performance
SELECT
    COUNT(*) AS total_sessions,
    COUNT(DISTINCT user_id) AS unique_users,
    SUM(purchase_completed = 'Yes') AS total_orders,
    ROUND(SUM(CASE
        WHEN purchase_completed = 'Yes' THEN order_value
        ELSE 0
    END), 2) AS gross_order_value,
    ROUND(SUM(CASE
        WHEN purchase_completed = 'Yes' THEN order_value - revenue
        ELSE 0
    END), 3) AS total_discounts,
    ROUND(SUM(revenue), 3) AS net_revenue,
    ROUND(AVG(CASE
        WHEN purchase_completed = 'Yes' THEN order_value
    END), 2) AS gross_aov,
    ROUND(SUM(revenue) /
        NULLIF(SUM(purchase_completed = 'Yes'), 0), 2
    ) AS net_revenue_per_order,
    ROUND(
        SUM(purchase_completed = 'Yes') * 100.0 / COUNT(*), 2
    ) AS purchase_conversion_rate
FROM product_data;


-- ==================================================
-- SECTION 03: SALES & REVENUE ANALYSIS
-- ==================================================

-- Query 1: Revenue by acquisition channel

SELECT
    channel,
    COUNT(*) AS total_sessions,
    SUM(purchase_completed = 'Yes') AS total_orders,
    ROUND(SUM(revenue), 3) AS total_revenue,
    ROUND(
        SUM(purchase_completed = 'Yes') * 100.0 / COUNT(*), 2
    ) AS purchase_conversion_rate
FROM product_data
GROUP BY channel
ORDER BY total_revenue DESC;

-- Query 2: Average Order Value by channel

SELECT
    channel,
    COUNT(*) AS total_orders,
    ROUND(AVG(order_value), 2) AS gross_aov,
    ROUND(AVG(revenue), 3) AS net_revenue_per_order
FROM product_data
WHERE purchase_completed = 'Yes'
GROUP BY channel
ORDER BY gross_aov DESC;

-- Query 3: Revenue by device

SELECT
    device,
    COUNT(*) AS total_sessions,
    SUM(purchase_completed = 'Yes') AS total_orders,
    ROUND(SUM(revenue), 3) AS total_revenue,
    ROUND(
        SUM(purchase_completed = 'Yes') * 100.0 / COUNT(*), 2
    ) AS purchase_conversion_rate
FROM product_data
GROUP BY device
ORDER BY total_revenue DESC;

-- Query 4: Monthly revenue trend

SELECT 
    month,
    COUNT(*) AS total_orders,
    ROUND(SUM(revenue), 3) AS total_revenue,
    ROUND(AVG(order_value), 2) AS gross_aov
FROM product_data
WHERE purchase_completed = 'Yes'
GROUP BY month
ORDER BY month;


-- Query 5: Discount impact on revenue

SELECT
    discount_applied,
    COUNT(*) AS total_orders,
    ROUND(SUM(order_value), 2) AS gross_order_value,
    ROUND(SUM(revenue), 3) AS net_revenue,
    ROUND(SUM(order_value - revenue), 3) AS discount_amount,
    ROUND(
        SUM(order_value - revenue) * 100.0 /
        NULLIF(SUM(order_value), 0), 2
    ) AS discount_percentage
FROM product_data
WHERE purchase_completed = 'Yes'
GROUP BY discount_applied;


-- ==================================================
-- SECTION 04: PRODUCT FUNNEL & CONVERSION ANALYSIS
-- ==================================================

-- Query 1: Customer funnel stage counts

SELECT
    COUNT(*) AS total_visitors,
    SUM(viewed_product = 'Yes') AS product_views,
    SUM(added_to_cart = 'Yes') AS add_to_cart,
    SUM(checkout_started = 'Yes') AS checkout_started,
    SUM(purchase_completed = 'Yes') AS completed_purchases
FROM product_data;

-- Query 2: Funnel stage conversion rates

SELECT
    ROUND(
        SUM(viewed_product = 'Yes') * 100.0 / COUNT(*), 2
    ) AS visit_to_view_rate,
    ROUND(
        SUM(added_to_cart = 'Yes') * 100.0 /
        NULLIF(SUM(viewed_product = 'Yes'), 0), 2
    ) AS view_to_cart_rate,
    ROUND(
        SUM(checkout_started = 'Yes') * 100.0 /
        NULLIF(SUM(added_to_cart = 'Yes'), 0), 2
    ) AS cart_to_checkout_rate,
    ROUND(
        SUM(purchase_completed = 'Yes') * 100.0 /
        NULLIF(SUM(checkout_started = 'Yes'), 0), 2
    ) AS checkout_to_purchase_rate,
    ROUND(
        SUM(purchase_completed = 'Yes') * 100.0 / COUNT(*), 2
    ) AS overall_conversion_rate
FROM product_data;

-- Query 3: Funnel conversion by acquisition channel

SELECT
    channel,
    COUNT(*) AS total_visitors,
    SUM(viewed_product = 'Yes') AS product_views,
    SUM(added_to_cart = 'Yes') AS add_to_cart,
    SUM(checkout_started = 'Yes') AS checkout_started,
    SUM(purchase_completed = 'Yes') AS completed_purchases,
    ROUND(
        SUM(added_to_cart = 'Yes') * 100.0 /
        NULLIF(SUM(viewed_product = 'Yes'), 0), 2
    ) AS view_to_cart_rate,
    ROUND(
        SUM(purchase_completed = 'Yes') * 100.0 / COUNT(*), 2
    ) AS overall_conversion_rate
FROM product_data
GROUP BY channel
ORDER BY view_to_cart_rate DESC;

-- Query 4: Funnel conversion by device

SELECT
    device,
    COUNT(*) AS total_visitors,
    SUM(viewed_product = 'Yes') AS product_views,
    SUM(added_to_cart = 'Yes') AS add_to_cart,
    SUM(checkout_started = 'Yes') AS checkout_started,
    SUM(purchase_completed = 'Yes') AS completed_purchases,
    ROUND(
        SUM(added_to_cart = 'Yes') * 100.0 /
        NULLIF(SUM(viewed_product = 'Yes'), 0), 2
    ) AS view_to_cart_rate,
    ROUND(
        SUM(purchase_completed = 'Yes') * 100.0 / COUNT(*), 2
    ) AS overall_conversion_rate
FROM product_data
GROUP BY device
ORDER BY view_to_cart_rate DESC;

-- Query 5: Funnel conversion by customer type

SELECT
    user_type,
    COUNT(*) AS total_visitors,
    SUM(viewed_product = 'Yes') AS product_views,
    SUM(added_to_cart = 'Yes') AS add_to_cart,
    SUM(checkout_started = 'Yes') AS checkout_started,
    SUM(purchase_completed = 'Yes') AS completed_purchases,
    ROUND(
        SUM(added_to_cart = 'Yes') * 100.0 /
        NULLIF(SUM(viewed_product = 'Yes'), 0), 2
    ) AS view_to_cart_rate,
    ROUND(
        SUM(purchase_completed = 'Yes') * 100.0 / COUNT(*), 2
    ) AS overall_conversion_rate
FROM product_data
GROUP BY user_type
ORDER BY overall_conversion_rate DESC;

-- Query 6: Funnel drop-off analysis

SELECT
    'Visit to Product View' AS funnel_stage,
    COUNT(*) AS starting_users,
    SUM(viewed_product = 'Yes') AS progressing_users,
    COUNT(*) - SUM(viewed_product = 'Yes') AS dropped_users,
    ROUND(
        (COUNT(*) - SUM(viewed_product = 'Yes')) * 100.0 /
        COUNT(*), 2
    ) AS drop_off_rate
FROM product_data

UNION ALL

SELECT
    'Product View to Cart',
    SUM(viewed_product = 'Yes'),
    SUM(added_to_cart = 'Yes'),
    SUM(viewed_product = 'Yes') - SUM(added_to_cart = 'Yes'),
    ROUND(
        (SUM(viewed_product = 'Yes') - SUM(added_to_cart = 'Yes')) * 100.0 /
        NULLIF(SUM(viewed_product = 'Yes'), 0), 2
    )
FROM product_data

UNION ALL

SELECT
    'Cart to Checkout',
    SUM(added_to_cart = 'Yes'),
    SUM(checkout_started = 'Yes'),
    SUM(added_to_cart = 'Yes') - SUM(checkout_started = 'Yes'),
    ROUND(
        (SUM(added_to_cart = 'Yes') - SUM(checkout_started = 'Yes')) * 100.0 /
        NULLIF(SUM(added_to_cart = 'Yes'), 0), 2
    )
FROM product_data

UNION ALL

SELECT
    'Checkout to Purchase',
    SUM(checkout_started = 'Yes'),
    SUM(purchase_completed = 'Yes'),
    SUM(checkout_started = 'Yes') - SUM(purchase_completed = 'Yes'),
    ROUND(
        (SUM(checkout_started = 'Yes') - SUM(purchase_completed = 'Yes')) * 100.0 /
        NULLIF(SUM(checkout_started = 'Yes'), 0), 2
    )
FROM product_data;

-- ==================================================
-- SECTION 05: CUSTOMER & RETENTION ANALYSIS
-- ==================================================

-- Query 1: Customer segment performance

SELECT
    user_type,
    COUNT(*) AS total_sessions,
    COUNT(DISTINCT user_id) AS unique_customers,
    SUM(purchase_completed = 'Yes') AS total_orders,
    COUNT(DISTINCT CASE
        WHEN purchase_completed = 'Yes' THEN user_id
    END) AS purchasing_customers,
    ROUND(SUM(revenue), 3) AS total_revenue,
    ROUND(
        SUM(purchase_completed = 'Yes') * 100.0 / COUNT(*), 2
    ) AS purchase_conversion_rate,
    ROUND(
        SUM(revenue) /
        NULLIF(COUNT(DISTINCT user_id), 0), 2
    ) AS revenue_per_customer
FROM product_data
GROUP BY user_type
ORDER BY total_revenue DESC;

-- Query 2: Repeat purchase analysis

SELECT
    CASE
        WHEN purchase_count = 1 THEN 'One-time Customer'
        ELSE 'Repeat Customer'
    END AS customer_segment,
    COUNT(*) AS total_customers,
    SUM(purchase_count) AS total_orders,
    ROUND(AVG(purchase_count), 2) AS avg_orders_per_customer
FROM (
    SELECT
        user_id,
        COUNT(*) AS purchase_count
    FROM product_data
    WHERE purchase_completed = 'Yes'
    GROUP BY user_id
) AS customer_orders
GROUP BY customer_segment
ORDER BY total_customers DESC;

-- Query 3: Revenue contribution by purchase frequency

SELECT
    CASE
        WHEN purchase_count = 1 THEN 'One-time Customer'
        ELSE 'Repeat Customer'
    END AS customer_segment,
    COUNT(*) AS total_customers,
    SUM(purchase_count) AS total_orders,
    ROUND(SUM(total_revenue), 3) AS total_revenue,
    ROUND(AVG(total_revenue), 2) AS revenue_per_customer
FROM (
    SELECT
        user_id,
        COUNT(*) AS purchase_count,
        SUM(revenue) AS total_revenue
    FROM product_data
    WHERE purchase_completed = 'Yes'
    GROUP BY user_id
) AS customer_orders
GROUP BY customer_segment
ORDER BY total_revenue DESC;

-- Query 4: Repeat purchase rate by first purchase month

WITH customer_purchase_dates AS (
    SELECT
        user_id,
        MIN(date) AS first_purchase_date,
        MAX(date) AS last_purchase_date
    FROM product_data
    WHERE purchase_completed = 'Yes'
    GROUP BY user_id
)
SELECT
    DATE_FORMAT(first_purchase_date, '%Y-%m') AS cohort_month,
    COUNT(*) AS first_time_customers,
    SUM(last_purchase_date > first_purchase_date) AS repeat_customers,
    ROUND(
        SUM(last_purchase_date > first_purchase_date) * 100.0 / COUNT(*),
        2
    ) AS repeat_purchase_rate
FROM customer_purchase_dates
GROUP BY cohort_month
ORDER BY cohort_month;

-- Query 5: Average days between first and second purchase

WITH first_purchase AS (
    SELECT
        user_id,
        MIN(date) AS first_purchase_date
    FROM product_data
    WHERE purchase_completed = 'Yes'
    GROUP BY user_id
),
first_repeat_purchase AS (
    SELECT
        f.user_id,
        f.first_purchase_date,
        MIN(p.date) AS first_repeat_date
    FROM first_purchase f
    JOIN product_data p
        ON f.user_id = p.user_id
       AND p.purchase_completed = 'Yes'
       AND p.date > f.first_purchase_date
    GROUP BY f.user_id, f.first_purchase_date
)
SELECT
    COUNT(*) AS repeat_customers,
    ROUND(AVG(DATEDIFF(first_repeat_date, first_purchase_date)), 2)
        AS average_days_to_repeat,
    MIN(DATEDIFF(first_repeat_date, first_purchase_date))
        AS minimum_days_to_repeat,
    MAX(DATEDIFF(first_repeat_date, first_purchase_date))
        AS maximum_days_to_repeat
FROM first_repeat_purchase;

-- Query 6: Customer quality by acquisition channel

SELECT
    channel,
    COUNT(DISTINCT user_id) AS total_customers,
    COUNT(DISTINCT CASE
        WHEN purchase_completed = 'Yes' THEN user_id
    END) AS purchasing_customers,
    SUM(purchase_completed = 'Yes') AS total_orders,
    ROUND(SUM(revenue), 3) AS total_revenue,
    ROUND(
        COUNT(DISTINCT CASE
            WHEN purchase_completed = 'Yes' THEN user_id
        END) * 100.0 / COUNT(DISTINCT user_id),
        2
    ) AS customer_purchase_rate,
    ROUND(
        SUM(revenue) / NULLIF(
            COUNT(DISTINCT CASE
                WHEN purchase_completed = 'Yes' THEN user_id
            END), 0
        ),
        2
    ) AS revenue_per_purchasing_customer,
    ROUND(
        SUM(revenue) / NULLIF(SUM(purchase_completed = 'Yes'), 0),
        2
    ) AS revenue_per_order
FROM product_data
GROUP BY channel
ORDER BY total_revenue DESC;

-- ==================================================
-- SECTION 06: DISCOUNT & PROMOTION ANALYSIS
-- ==================================================

-- Query 1: Discount vs Non-Discount Performance

SELECT
    discount_applied,
    COUNT(*) AS total_sessions,
    SUM(purchase_completed = 'Yes') AS total_orders,
    ROUND(
        SUM(purchase_completed = 'Yes') * 100.0 / COUNT(*),
        2
    ) AS purchase_conversion_rate,
    ROUND(
        SUM(CASE
            WHEN purchase_completed = 'Yes' THEN order_value
            ELSE 0
        END), 2
    ) AS gross_order_value,
    ROUND(SUM(revenue), 2) AS net_revenue,
    ROUND(
        SUM(CASE
            WHEN purchase_completed = 'Yes' THEN order_value - revenue
            ELSE 0
        END), 2
    ) AS discount_amount,
    ROUND(
        AVG(CASE
            WHEN purchase_completed = 'Yes' THEN revenue
        END), 2
    ) AS net_revenue_per_order
FROM product_data
GROUP BY discount_applied
ORDER BY discount_applied;

-- Query 1A: Discount assignment validation

SELECT
    discount_applied,
    purchase_completed,
    COUNT(*) AS total_records
FROM product_data
GROUP BY
    discount_applied,
    purchase_completed
ORDER BY
    discount_applied,
    purchase_completed;

-- Query 2: Discount contribution to total revenue

SELECT
    discount_applied,
    SUM(purchase_completed = 'Yes') AS total_orders,
    ROUND(SUM(revenue), 2) AS net_revenue,
    ROUND(
        SUM(revenue) * 100.0 /
        (SELECT SUM(revenue)
         FROM product_data),
        2
    ) AS revenue_contribution_percentage,
    ROUND(
        SUM(purchase_completed = 'Yes') * 100.0 /
        (SELECT SUM(purchase_completed = 'Yes')
         FROM product_data),
        2
    ) AS order_contribution_percentage
FROM product_data
GROUP BY discount_applied
ORDER BY discount_applied;

-- Query 3: Average Discount Analysis

SELECT
    COUNT(*) AS discounted_orders,
    ROUND(SUM(order_value), 2) AS total_gross_value,
    ROUND(SUM(revenue), 2) AS total_net_revenue,
    ROUND(SUM(order_value - revenue), 2) AS total_discount,
    ROUND(AVG(order_value - revenue), 2) AS average_discount_per_order,
    ROUND(
        SUM(order_value - revenue) * 100.0 /
        NULLIF(SUM(order_value), 0),
        2
    ) AS average_discount_percentage
FROM product_data
WHERE
    purchase_completed = 'Yes'
    AND discount_applied = 'Yes';

-- Query 4: Discount Performance by Channel

SELECT
    channel,
    COUNT(*) AS discounted_orders,
    ROUND(SUM(order_value), 2) AS gross_order_value,
    ROUND(SUM(revenue), 2) AS net_revenue,
    ROUND(SUM(order_value - revenue), 2) AS total_discount,
    ROUND(AVG(revenue), 2) AS net_revenue_per_order,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*)
         FROM product_data
         WHERE purchase_completed = 'Yes'
           AND discount_applied = 'Yes'),
        2
    ) AS discount_order_share
FROM product_data
WHERE purchase_completed = 'Yes'
  AND discount_applied = 'Yes'
GROUP BY channel
ORDER BY net_revenue DESC;

-- Query 5: Discount Performance by Device

SELECT
    device,
    COUNT(*) AS discounted_orders,
    ROUND(SUM(revenue), 2) AS net_revenue,
    ROUND(AVG(revenue), 2) AS net_revenue_per_order,
    ROUND(SUM(order_value - revenue), 2) AS total_discount,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*)
         FROM product_data
         WHERE purchase_completed = 'Yes'
           AND discount_applied = 'Yes'),
        2
    ) AS discount_order_share
FROM product_data
WHERE purchase_completed = 'Yes'
  AND discount_applied = 'Yes'
GROUP BY device
ORDER BY net_revenue DESC;    

-- Query 6: Discount Performance by Customer Type

SELECT
    user_type,
    COUNT(*) AS discounted_orders,
    COUNT(DISTINCT user_id) AS unique_customers,
    ROUND(SUM(revenue), 2) AS net_revenue,
    ROUND(AVG(revenue), 2) AS net_revenue_per_order,
    ROUND(SUM(order_value - revenue), 2) AS total_discount,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*)
         FROM product_data
         WHERE purchase_completed = 'Yes'
           AND discount_applied = 'Yes'),
        2
    ) AS discount_order_share
FROM product_data
WHERE purchase_completed = 'Yes'
  AND discount_applied = 'Yes'
GROUP BY user_type
ORDER BY net_revenue DESC;

-- Query 7: Monthly Discount Performance

SELECT
    month,
    COUNT(*) AS discounted_orders,
    ROUND(SUM(order_value), 2) AS gross_order_value,
    ROUND(SUM(revenue), 2) AS net_revenue,
    ROUND(SUM(order_value - revenue), 2) AS total_discount,
    ROUND(AVG(revenue), 2) AS net_revenue_per_order,
    ROUND(
        SUM(order_value - revenue) * 100.0 /
        NULLIF(SUM(order_value), 0),
        2
    ) AS discount_percentage
FROM product_data
WHERE purchase_completed = 'Yes'
  AND discount_applied = 'Yes'
GROUP BY month
ORDER BY month;

-- Query 8: Monthly Discount vs Non-Discount Performance

SELECT
    month,
    discount_applied,
    COUNT(*) AS total_orders,
    ROUND(SUM(revenue), 2) AS net_revenue,
    ROUND(AVG(revenue), 2) AS net_revenue_per_order,
    ROUND(SUM(order_value - revenue), 2) AS total_discount
FROM product_data
WHERE purchase_completed = 'Yes'
GROUP BY
    month,
    discount_applied
ORDER BY
    month,
    discount_applied;

-- Query 9: Discount Performance by Campaign Type

SELECT
    campaign_type,
    COUNT(*) AS discounted_orders,
    ROUND(SUM(order_value), 2) AS gross_order_value,
    ROUND(SUM(revenue), 2) AS net_revenue,
    ROUND(AVG(revenue), 2) AS net_revenue_per_order,
    ROUND(SUM(order_value - revenue), 2) AS total_discount,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*)
         FROM product_data
         WHERE purchase_completed = 'Yes'
           AND discount_applied = 'Yes'),
        2
    ) AS discounted_order_share
FROM product_data
WHERE purchase_completed = 'Yes'
  AND discount_applied = 'Yes'
GROUP BY campaign_type
ORDER BY net_revenue DESC;    


