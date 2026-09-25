from prefect import flow, task
import subprocess
import sys   # sys.executable = the exact python running this script (robust vs bare "python")

# Each @task is one step in the pipeline.
# retries=2 means: if this step fails, try again up to 2 more times.

@task(retries=2)
def load_claims():
    subprocess.run([sys.executable, "batch/load_claims_incremental.py"], check=True)

@task(retries=2)
def load_policies():
    subprocess.run([sys.executable, "batch/load_policies.py"], check=True)

@task
def dbt_run():
    subprocess.run(
        ["/Users/ankita/data-platform/.venv/bin/dbt", "run", "--profiles-dir", "."],
        cwd="transform", check=True,
    )

@task
def dbt_test():
    subprocess.run(
        ["/Users/ankita/data-platform/.venv/bin/dbt", "test", "--profiles-dir", "."],
        cwd="transform", check=True,
    )

# The @flow ties the tasks together. Calling tasks directly (no .submit())
# runs them SEQUENTIALLY, in order — which is exactly what we want, because
# DuckDB is single-writer (parallel writes would clash on the lock).
@flow(name="insurance-pipeline", log_prints=True)
def insurance_pipeline():
    load_claims()     # 1. load claims first
    load_policies()   # 2. then policies (no lock clash)
    dbt_run()         # 3. then transform (dbt can't run before data is loaded)
    dbt_test()        # 4. then validate

if __name__ == "__main__":
    insurance_pipeline()