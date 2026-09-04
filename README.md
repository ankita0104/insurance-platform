# Insurance Data Platform

An end-to-end data engineering platform for insurance claims and policies — built with
the modern data stack. It ingests daily file drops, loads them idempotently, transforms
them with dbt into a tested dimensional model, monitors data quality, and orchestrates
the whole flow on a schedule.

> **Business context:** insurance data typically arrives as daily batch file exports
> (not APIs). This platform mirrors that pattern and turns raw claims/policies into
> trustworthy, analytics-ready tables — with data quality enforced at every step.

---

## Architecture

```
 landing/ (daily CSV drops)
     │
     ▼   Python loaders (idempotent + incremental)
 raw_claims ── raw_policies          ← bronze (raw, as-received)
     │
     ▼   dbt (tested transformations)
 stg_claims ── stg_policies          ← staging (cleaned, enriched)
     │
     ▼   dbt (marts / star schema)
 fct_claims ─┬─ dim_policy
             ├─ dim_claim_type        ← Kimball star schema
             └─ dim_date
     │
     ▼
 analytics: loss ratio / exposure by product, state, time

 Orchestrated by Prefect (scheduled DAG + retries)
 Data quality monitored by an observability suite (freshness/volume/schema/distribution)
```

## Key features

- **Idempotent, incremental ingestion** — primary keys + `ON CONFLICT DO NOTHING` +
  `loaded_at` audit timestamps, so re-runs never create duplicate claims (preventing
  double-counted payouts / reserve misstatements).
- **Tested dbt transformation layer** — staging → marts, with `not_null`, `unique`, and
  `accepted_values` tests enforcing data quality on every build.
- **Kimball star schema** — `fct_claims` fact (claim grain) with `dim_policy`,
  `dim_claim_type`, `dim_date` dimensions for clean analytical queries.
- **Data observability suite** — freshness, volume, schema, and distribution checks
  (metric → expectation → status), plus lineage via dbt.
- **Orchestration** — Prefect DAG with dependencies, automatic retries, and cron scheduling.

## Tech stack

Python · dbt · DuckDB · Prefect · SQL · Git

## Project structure

```
batch/         Python loaders (ingestion, idempotent/incremental)
transform/     dbt project (staging models, marts / star schema, tests)
quality/       data observability checks
landing/       sample daily CSV file drops (synthetic data)
orchestrate.py Prefect flow that runs the whole pipeline
```

## Running it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install duckdb prefect
# dbt-duckdb for the transform layer

# run the full pipeline (ingest -> dbt run -> dbt test)
python orchestrate.py
```

---

*Note: all data in this repository is synthetic and generated for demonstration.*
