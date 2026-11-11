# Initiative PRD: Review Discount Strategy

# 1. Summary
Priority: P3 — validate economics and behavior before broad changes  
Problem area: Discount use, conversion, and revenue quality

# 2. Problem statement
Discounted sessions may behave differently from non-discounted sessions, but observed differences alone do not prove discounts caused the outcome. ProductSignal needs to understand whether a discount generates incremental profitable demand or simply reduces revenue on purchases that would have occurred anyway.
Current analysis shows ₹9,81,240.79 in total discounts across completed orders where discounts were applied. However, the available data does not establish whether these discounts generated incremental purchases or reduced revenue on purchases that would have occurred anyway.

# 3. User and need
User: Growth/product manager or business owner.  
Need: Choose offers based on incremental customer and financial value, not conversion lift alone.

# 4. Hypotheses to investigate
- Discounts may encourage cart creation or purchase completion.
- Some offers may subsidize purchases that would have happened without them.
- Discount response may vary by channel, device, or user type.
- Larger discounts may increase conversion while reducing order value or contribution margin.

Treat these as hypotheses until tested with reliable data.

# 5. Proposed solution
- Validate discount flags, eligibility, and data definitions.
- Compare funnel rate, AOV, revenue per eligible session, and order value across discount segments.
- Obtain discount amount and cost/margin data if available.
- With the current dataset, limit conclusions to descriptive comparisons of completed orders. Do not infer incremental conversion or profitability from discount and non-discount groups.
- Run a controlled experiment or a defensible holdout design before attributing incremental impact.
- Consider targeted offers or non-price incentives only if evidence supports them.


# 6. Requirements
- Document what `discount_applied` means and whether it indicates eligibility, exposure, or actual redemption.
- Report sample sizes and denominators for discount/non-discount groups.
- Separate descriptive comparison from causal effect.
- Include revenue and margin/cost measures where available.
- Record assumptions for any scenario model.
- Do not recommend scaling a discount based only on a higher conversion rate.

# 7. Metrics
Primary KPI: Revenue per eligible session; use incremental contribution profit as the decision metric when cost data is available.  
Current measurement limitation: Revenue per eligible session and incremental contribution profit cannot be reliably evaluated without discount eligibility/exposure data and the necessary cost information.
Secondary: Purchase conversion, AOV, order value, add-to-cart rate.  
Guardrails: Contribution margin, discount cost, refund/cancellation rate, and customer behavior after the promotion where data permits.

# 8. Experiment design
- Define eligible audience and offer before launch.
- Control: No offer or current offer, depending on the business question.
- Variant: A clearly specified discount or alternative incentive.
- Randomize eligible users where feasible and prevent cross-group contamination.
- Set sample size, duration, and analysis plan before reading results.
- Compare incremental outcomes, including costs—not just raw revenue.

# 9. Acceptance criteria
- Discount semantics and data quality are verified.
- Segment sizes and metric denominators are reported.
- The analysis explicitly states that observational differences are not causal proof.
- Profitability claims use defensible cost inputs.
- The final recommendation states whether to scale, target, modify, or stop the offer, with evidence.

# 10. Risks
Discount-related data may be synthetic or semantically ambiguous. If the dataset does not contain discount amount, cost, or margin, the project must not claim to have measured true discount profitability or ROI.
