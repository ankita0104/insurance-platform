
  
    
    

    create  table
      "insurance"."main"."dim_claim_type__dbt_tmp"
  
    as (
      select distinct
    claim_type
from "insurance"."main"."stg_claims"
order by claim_type
    );
  
  