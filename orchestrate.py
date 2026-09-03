from prefect import flow, task
import subprocess

# Each @task is one step in the pipeline.
# retries=2 means: if this step fails, try again up to 2 more times.

@task(retries=2)
def load_claims():
    subprocess.run(["python", "batch/load_claims_incremental.py"], check=True)

@task(retries=2)
def load_policies():
    subprocess.run(["python", "batch/load_policies.py"], check=True)

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

# The @flow ties the tasks together and defines their ORDER via dependencies.
@flow(name="insurance-pipeline", log_prints=True)
def insurance_pipeline():
    # these two run first (independent)
    claims = load_claims.submit()
    policies = load_policies.submit(wait_for=[claims])   # policies waits for claims -> no lock clash

    run = dbt_run.submit(wait_for=[claims, policies])
    test = dbt_test.submit(wait_for=[run])
    test.result()

if __name__ == "__main__":
    insurance_pipeline()