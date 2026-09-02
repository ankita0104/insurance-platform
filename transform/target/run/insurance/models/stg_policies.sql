
  
    
    

    create  table
      "insurance"."main"."stg_policies__dbt_tmp"
  
    as (
      select
    policy_id,
    policyholder,
    state,
    product_type,
    annual_premium,
    start_date,
    status,

    case
        when annual_premium < 1000 then 'budget'
        when annual_premium < 2500 then 'standard'
        else 'premium'
    end as premium_tier,

    loaded_at
from raw_policies
    );
  
  