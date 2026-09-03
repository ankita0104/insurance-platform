select distinct
    claim_date                          as date_day,
    extract(year    from claim_date)    as year,
    extract(month   from claim_date)    as month,
    extract(quarter from claim_date)    as quarter,
    dayname(claim_date)                 as day_of_week
from "insurance"."main"."stg_claims"
order by date_day