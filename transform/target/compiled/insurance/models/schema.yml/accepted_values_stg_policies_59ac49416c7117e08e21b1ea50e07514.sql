
    
    

with all_values as (

    select
        premium_tier as value_field,
        count(*) as n_records

    from "insurance"."main"."stg_policies"
    group by premium_tier

)

select *
from all_values
where value_field not in (
    'budget','standard','premium'
)


