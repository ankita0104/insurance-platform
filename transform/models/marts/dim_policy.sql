select
    policy_id,          -- the key other tables join to
    policyholder,
    state,
    product_type,
    premium_tier,
    annual_premium,
    status
from {{ ref('stg_policies') }}
