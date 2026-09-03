select
    claim_id,                       -- the fact's own key (one row per claim)

    -- foreign keys -> dimensions
    policy_id,                      -- joins to dim_policy
    claim_type,                     -- joins to dim_claim_type
    claim_date,                     -- joins to dim_date

    -- measures (the numbers we analyze)
    claim_amount,
    severity_band,

    status
from "insurance"."main"."stg_claims"