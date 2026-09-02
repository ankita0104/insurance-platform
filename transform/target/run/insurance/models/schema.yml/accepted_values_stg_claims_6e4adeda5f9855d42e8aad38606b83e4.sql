
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        severity_band as value_field,
        count(*) as n_records

    from "insurance"."main"."stg_claims"
    group by severity_band

)

select *
from all_values
where value_field not in (
    'small','medium','large','catastrophic'
)



  
  
      
    ) dbt_internal_test