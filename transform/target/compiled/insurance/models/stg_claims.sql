select
      claim_id,
      policy_id,
      claim_date,
      claim_type,
      claim_amount,
      status, 
      state,

      case
          when claim_amount < 1000  then 'small'
          when claim_amount < 10000 then 'medium'
          when claim_amount < 30000 then 'large'
          else 'catastrophic'
      end as severity_band,
  
      loaded_at

  from raw_claims