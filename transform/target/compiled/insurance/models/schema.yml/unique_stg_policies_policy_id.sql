
    
    

select
    policy_id as unique_field,
    count(*) as n_records

from "insurance"."main"."stg_policies"
where policy_id is not null
group by policy_id
having count(*) > 1


