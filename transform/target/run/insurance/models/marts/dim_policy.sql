
  
    
    

    create  table
      "insurance"."main"."dim_policy__dbt_tmp"
  
    as (
      select
    policy_id,          -- the key other tables join to
    policyholder,
    state,
    product_type,
    premium_tier,
    annual_premium,
    status
from "insurance"."main"."stg_policies"
    );
  
  