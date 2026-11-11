from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

# ProductSignal A/B test design
baseline_conversion = 0.3487
target_conversion = 0.3987

significance_level = 0.05
statistical_power = 0.80

# Calculate standardized effect size 
effect_size = proportion_effectsize(
    baseline_conversion,
    target_conversion
)

# Estimate sample size for two equally sized groups
power_analysis = NormalIndPower()

sample_size_per_group = power_analysis.solve_power(
    effect_size = effect_size,
    power = statistical_power,
    alpha = significance_level,
    ratio = 1.0,
    alternative = "two-sided"
)

sample_size_per_group = int(sample_size_per_group) + 1
total_sample_size = sample_size_per_group * 2

print("PRODUCTSIGNAL -A/B TEST DESIGN")
print("-" * 40)

print(f"Control baseline: {baseline_conversion:.2%}")
print(f"Target Conversion: {target_conversion:.2%}")
print(
    f"Target absolute lift:"
    f"{target_conversion - baseline_conversion:.2%}"
)
print(f"Siginificance level: {significance_level:.0%}")
print(f"Statistical power: {statistical_power:.0%}")
print(f"Required sample per group: {sample_size_per_group:,}")
print(f"Total required sample: {total_sample_size:,}")

import math
# Experiment duration estimate

# Update this with the average number of eligible
# product-view sessions available per day.
daily_eligible_sessions = 1000

# Assume 50/50 traffic allocation
traffic_allocation = 0.50

daily_sessions_per_group = (
    daily_eligible_sessions * traffic_allocation
)

estimated_days = math.ceil(
    sample_size_per_group / daily_sessions_per_group
)

print("EXPERIMENT DURATION ESTIMATE")
print("-" * 40)
print(f"Eligible session per day: {daily_eligible_sessions:,}")
print(f"Traffic allocation per group: {traffic_allocation:.0%}")
print(f"Sessions per group per day: {daily_sessions_per_group:,.0f}")
print(f"Estimated collection time: {estimated_days} days")

from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep

# Example experiment results
# These are simulated practice values, NOT real experiment data.

control_visitors = 5000
control_conversions = 1744

variant_visitors = 5000
variant_conversions = 1994

# Validate experiment inputs
if control_visitors <=0 or variant_visitors <=0:
    raise ValueError("Visitor counts must be greater than zero.")

if not 0 <= control_conversions <= control_visitors:
    raise ValueError("Invalid control conversion count.")

if not 0 <= variant_conversions <= variant_visitors:
    raise ValueError("Invalid variant conversion count.")

# Calculate conversion rates
control_rate = control_conversions / control_visitors
variant_rate = variant_conversions / variant_visitors

absolute_lift = variant_rate - control_rate

relative_lift = (
    absolute_lift / control_rate
    if control_rate > 0
    else float("nan")
)

# Two-proportion z-test
z_statistic, p_value = proportions_ztest(
    [variant_conversions, control_conversions],
    [variant_visitors, control_visitors],
    alternative = "two-sided"
)

# 95% confidence interval for variant minus control
ci_lower, ci_upper = confint_proportions_2indep(
    variant_conversions,
    variant_visitors,
    control_conversions,
    control_visitors,
    method = "newcomb",
    compare = "diff",
    alpha = 0.05
)

# Display results 
print("A/B TEST EVALUATION")
print("-" * 45)
print(f"Control conversion: {control_rate:.2%}")
print(f"Variant conversion: {variant_rate:.2%}")
print(f"Absolute lift: {absolute_lift * 100:.2f}")
print(f"Relative lift: {relative_lift:.2%}")
print(f"Z-statistic: {z_statistic:.3f}")
print(f"P-value: {p_value:.6f}")
print(
    f"95% confidence interval:"
    f"[{ci_lower * 100:.2f}, {ci_upper * 100:.2f}]"
    "percentage points"
)

# Interpret statistical evidence
statistically_significant = p_value < 0.05
ci_excludes_zero = ci_lower > 0 or ci_upper < 0

if statistically_significant:
    print("Statistical result: Significance difference detected.")
else:
    print("Statistical result: Insufficient evidence of a difference.")

print(f"Confidence interval excludes zero: {ci_excludes_zero}")
print("Reminder: Statistical significance does not prove business value.")

# Business decision layer
control_revenue_per_visitor = 72.00
variant_revenue_per_visitor = 70.50

# Maximum acceptable revenue decline: 2%
maximum_revenue_decline = 0.02

revenue_change = (
    (variant_revenue_per_visitor - control_revenue_per_visitor)
    / control_revenue_per_visitor
    if control_revenue_per_visitor > 0
    else 0
)

print(f"Revenue per visitor change: {revenue_change:.2%}")

# Final business decision logic
conversion_improved = variant_rate > control_rate
statistically_significant = p_value < 0.05

revenue_guardrail_passed = (
    revenue_change >= -maximum_revenue_decline
)

print("FINAL BUSINESS DECISION")
print("-" * 45)

if not revenue_guardrail_passed:
    print("Decision: Don not ship yet.")
    print("Reason: Revenue-per-visitor quadrail failed.")
elif not statistically_significant:
    print("Decision: Insufficient evidenc; do not ship yet.")
    print("Reason: Conversion difference is not statistically significant.")
elif not conversion_improved:
    print("Decision: Do not ship the variant.")
    print("Reason: Conversion did not improve.")
else:
    print("Decision: Consider shipping the variant.")
    print("Reason: Conversion improved significantly and the revenue guardrail passed.")
    print("Check experiemnt quality and all other business guardrails first.")        

# Scenario testing: validate business decision logic
print("SCENARIO TESTING")
print("-" * 45)

scenarios = [
    {
        "name": "Scenario 1: Successful variant",
        "control_rate": 0.35,
        "variant_rate": 0.40,
        "p_value": 0.01,
        "revenue_change": 0.03
    },
    {
        "name": "Scenario 2: Insufficient evidence",
        "control_rate": 0.35,
        "variant_rate": 0.36,
        "p_value": 0.20,
        "revenue_change": 0.01
    },
    {
        "name": "Scenario 3: Conversion improves, revenue declines",
        "control_rate": 0.35,
        "variant_rate": 0.40,
        "p_value": 0.01,
        "revenue_change": -0.03
    }
]

for scenario in scenarios:
    conversion_improved = (
        scenario["variant_rate"] > scenario["control_rate"]
    )
    statistically_significant = scenario["p_value"] < 0.05
    revenue_guardrail_passed = scenario["revenue_change"] >= -0.02

    if(
        conversion_improved
        and statistically_significant
        and revenue_guardrail_passed
    ):
        decision = "Consider shipping; verify other guardrails"
    elif not revenue_guardrail_passed:
        decision = "Do not ship yet: revenue guardrail failed"
    elif not statistically_significant:
        decision = "Insufficient evidence: do not ship yet"
    else:
        decision = "Investigate: conversion did not improve"

    print(f"{scenario['name']}")
    print(f"Decision: {decision}")    

# Export A/B testing reults for the ProductSignal app
import pandas as pd
from pathlib import Path

# Locate the project's data folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_ROOT / "data"/ "ab_testing.csv"

# Recalculate the main experiment's decision
main_conversion_improved = variant_rate > control_rate

main_revenue_guardrail_passed = (
    revenue_change >= -maximum_revenue_decline
)

if not main_revenue_guardrail_passed:
    main_decision = "Do Not Ship - Revenue Guardrail failed"
elif not statistically_significant or not ci_excludes_zero:
    main_decision = "Do Not Ship Yet - Insufficient Evidence"
elif not main_conversion_improved:
    main_decision = "Do Not Ship - No Conversion Improvement"
else:
    main_decision = "Consider Shipping - Validate Guardrails"

# Save the main experiment results
results = {
    "data_type": "Simulated practice data",
    "control_visitors": control_visitors,
    "control_conversions": control_conversions,
    "variant_visitors": variant_visitors,
    "variant_conversions": variant_conversions,
    "control_conversion_rate": control_rate,
    "variant_conversion_rate": variant_rate,
    "absolute_lift": absolute_lift,
    "relative_lift": relative_lift,
    "p_value": p_value,
    "ci_lower": ci_lower,
    "ci_upper": ci_upper,
    "control_revenue_per_visitor": control_revenue_per_visitor,
    "variant_revenue_per_visitor": variant_revenue_per_visitor,
    "revenue_change": revenue_change,
    "statistically_significant": p_value < significance_level,
    "revenue_guardrail_passed": main_revenue_guardrail_passed,
    "decision": main_decision,
}

results_df = pd.DataFrame([results])
results_df.to_csv(OUTPUT_FILE, index = False)

print(f"A/B test results exported to: {OUTPUT_FILE}")


print("CSV column names:")
print(results_df.columns.tolist())

print("Duplicate column names:")
print(results_df.columns[results_df.columns.duplicated()].tolist())

    