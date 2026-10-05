"""
claims_transform.py
--------------------
PySpark job for the insurance data platform's distributed processing layer.

Reads raw insurance claims, classifies claim severity, and produces aggregated
claim metrics by status and severity. Writes the output as Parquet (the columnar
format used across big-data and lakehouse platforms).

Run:  python spark/claims_transform.py
"""

from pyspark.sql import SparkSession


def main():
    # Start the Spark engine (local mode = this machine's cores; the same code
    # runs on a cluster by changing only the master).
    spark = (
        SparkSession.builder
        .master("local[*]")
        .appName("claims_transform")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")

    # 1) Ingest raw claims and expose them to Spark SQL as a table.
    claims = spark.read.csv(
        "landing/claims_2026-08-22.csv", header=True, inferSchema=True
    )
    claims.createOrReplaceTempView("claims")

    # 2) Transform: enrich each claim with a severity classification.
    enriched = spark.sql("""
        SELECT
            claim_id, policy_id, claim_date, claim_type, claim_amount, status, state,
            CASE
                WHEN claim_amount < 1000  THEN 'small'
                WHEN claim_amount < 10000 THEN 'medium'
                WHEN claim_amount < 30000 THEN 'large'
                ELSE 'catastrophic'
            END AS severity_band
        FROM claims
    """)
    enriched.createOrReplaceTempView("claims_enriched")

    # 3) Aggregate: claim metrics by status and severity band.
    metrics = spark.sql("""
        SELECT
            
            state,
            count(*)                     AS claim_count,
            round(sum(claim_amount), 2)  AS total_amount,
            round(avg(claim_amount), 2)  AS avg_amount
        FROM claims_enriched
        GROUP BY state
        ORDER BY total_amount DESC
    """)
    metrics.show(truncate=False)

    # 4) Write the aggregated output as Parquet (columnar, partition-friendly).
    metrics.write.mode("overwrite").parquet("data/claims_metrics")
    print("Wrote aggregated claim metrics to data/claims_metrics/ (Parquet)")

    spark.stop()


if __name__ == "__main__":
    main()
