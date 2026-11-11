# ProductSignal
### AI-Powered Product Growth & Decision Intelligence System

**Tagline:** Turn product data into measurable business decisions.

## 1. Project Overview

ProductSignal is an AI-powered product analytics and decision-support system built around an e-commerce business dataset.

It helps analyze the customer journey, identify conversion bottlenecks, evaluate business performance, and translate analytical findings into actionable product recommendations.

The project combines Python, SQL, Streamlit, product management principles, A/B testing, and Gemini AI to demonstrate how data can support product and business decisions.

## 2. Business Problem

E-commerce businesses need to understand more than just their revenue and order numbers.

They need to identify:
- Where customers drop off during the purchasing journey.
- Which marketing channels generate the most revenue.
- How discounts relate to revenue performance.
- Whether customers return for repeat purchases.
- Which product improvements deserve priority.
- How proposed changes should be validated through experimentation.

ProductSignal addresses these questions through structured analysis and a decision-support dashboard.

## 3. Project Objectives

- Analyze the e-commerce customer conversion funnel.
- Evaluate revenue and channel performance.
- Understand customer purchasing and retention patterns.
- Assess discount and promotion performance.
- Identify high-impact product opportunities.
- Design A/B testing scenarios.
- Use AI to generate business insights and recommendations.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data cleaning, analysis and business logic |
| Pandas | Data manipulation and analysis |
| SQL (MySQL) | Business queries and KPI analysis |
| Streamlit | Interactive analytics dashboard |
| Plotly | Data visualization |
| Gemini API | AI-powered business insights |
| Statsmodels | A/B test sample-size and statistical calculations |

## 5. Dataset Overview

- **Dataset type:** Synthetic e-commerce dataset
- **Total records:** 120,000
- **Number of columns:** 17
- **Time period:** July–December 2025

The dataset contains information relating to:
- Users and sessions
- Dates and months
- Marketing channels and campaigns
- Device types and user types
- Product funnel events
- Discount application
- Order values and revenue

Data cleaning and validation were performed before analysis.

## 6. Key Business Findings

### Conversion Funnel

| Funnel Stage | Sessions |
|---|---:|
| Product Views | 77,870 |
| Added to Cart | 27,156 |
| Checkout Started | 16,234 |
| Completed Purchases | 8,181 |

Conversion rates:

- View to Cart: 34.87%
- Cart to Checkout: 59.78%
- Checkout to Purchase: 50.39%
- Overall conversion: 6.82%

The largest absolute funnel drop-off occurs between product views and cart additions.

### Financial Performance

| Metric | Result |
|---|---:|
| Net Revenue | ₹17,016,599.15 |
| Completed Orders | 8,181 |
| Gross Average Order Value | ₹2,199.96 |
| Net Revenue per Order | ₹2,080.01 |
| Total Discount | ₹981,240.79 |

### Channel Performance

- Paid Ads generated the highest total revenue.
- Email had the highest purchase conversion rate.
- Social had the highest gross average order value.
- Organic was the second-largest revenue contributor.

### Customer Insights

- One-time customers: 8,097
- Repeat customers: 42
- Repeat customers generated 84 orders.

The low observed repeat-customer count highlights a potential customer-retention opportunity.

### Monthly Performance

Monthly revenue was highest in July 2025 and lowest in December 2025, indicating a declining revenue trend across the observed period.

## 7. Product Opportunities & Recommendations

The analysis identified three major product opportunities:

**1. Product Page Conversion Optimization**

Improve the transition from product views to cart additions by investigating product information, pricing clarity, trust signals, and calls to action.

**2. Checkout Optimization**

Investigate checkout-stage drop-offs and identify potential friction in the purchasing journey.

**3. Discount Strategy**

Evaluate discount usage alongside order value and net revenue to understand its relationship with purchasing performance.

These opportunities are translated into product requirements and recommendations through dedicated PRDs.

## 8. Interactive Dashboard

ProductSignal includes a Streamlit dashboard with six analytical pages and an additional AI Insights page.

| Dashboard Page | Purpose |
|---|---|
| Overview | Overall business KPIs and performance |
| Funnel Analysis | Customer journey and conversion rates |
| Channel Performance | Revenue and conversion by channel |
| Customer Insights | User types and device-level behavior |
| Decision Center | Prioritized business opportunities |
| A/B Testing | Experiment results and decision evaluation |
| AI Insights | AI-generated business analysis and recommendations |

The dashboard also includes interactive filters for marketing channels, devices, and date ranges.

## 9. AI Integration

ProductSignal integrates Google's Gemini API to provide an AI-assisted business analysis experience.

The AI layer:
- Receives calculated aggregate business metrics.
- Interprets sales and funnel performance.
- Identifies potential business opportunities.
- Generates product and business recommendations.
- Suggests KPIs for further monitoring.
- Responds to user questions about the supplied metrics.

Python remains responsible for calculating the metrics, while Gemini assists with interpreting the results.

The AI output is intended to support decision-making, not replace analytical validation or business judgment.

## 10. A/B Testing

An A/B testing framework was developed to evaluate a proposed improvement in the View-to-Cart conversion rate.

Experiment design:

- Baseline conversion: 34.87%
- Target conversion: 39.87%
- Significance level: 0.05
- Statistical power: 80%
- Required sample size: 1,469 per group

A revenue guardrail was included to prevent shipping a variant that improves conversion while negatively affecting revenue per visitor.

The results are simulated practice results, not outcomes from a live experiment.

## 11. Documentation

ProductSignal includes the following product documentation:

- `PRD_Master.md` — Product vision, users, scope, requirements, metrics, assumptions, and roadmap.
- `PRD_Product_Page_Conversion.md` — Product-view-to-cart conversion improvement.
- `PRD_Checkout_Optimization.md` — Checkout friction reduction.
- `PRD_Discount_Strategy.md` — Discount effectiveness and economics.

## 12. Project Scripts

The project includes separate Python scripts for:

- Data cleaning and validation
- Funnel analysis
- Financial analysis
- Product insights
- A/B testing
- Business decision generation

These scripts support the analytical workflow behind the dashboard.

## 13. How to Run

1. Clone or download the repository.
2. Create and activate a Python virtual environment.
3. Install the required project dependencies.
4. Configure the Gemini API key in Streamlit secrets.
5. Run the Streamlit application:

```bash
streamlit run app.py
```

## 14. Limitations & Assumptions

- The project uses a synthetic educational e-commerce dataset.
- Observed associations do not establish causality.
- The 34.87% to 39.87% conversion improvement is a scenario target, not a guaranteed outcome.
- A/B testing results are simulated practice results, not live experiment outcomes.
- Customer acquisition cost, advertising spend, and contribution margin data are unavailable.
- Profitability and marketing ROI cannot be conclusively evaluated without cost data.
- AI-generated recommendations require human review and further validation.

## 15. Project Purpose

ProductSignal demonstrates the application of data analytics, SQL, product thinking, experimentation, and AI integration to practical business problems.

The objective is not simply to report what happened, but to identify opportunities, recommend improvements, and define how those improvements can be measured and validated.

---

**ProductSignal — Turn product data into measurable business decisions.**