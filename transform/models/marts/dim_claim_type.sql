select distinct
    claim_type
from {{ ref('stg_claims') }}
order by claim_type