"""
claims_policy_enrichment.py
---------------------------
Joins insurance claims to their policies and produces enriched analytics:
claim metrics by product line (line of business). Part of the platform's
Spark processing layer.
"""

from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .master("local[*]")
        .appName("claims_policy_enrichment")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")

    # 1) Read BOTH sources and expose them to Spark SQL.
    claims = spark.read.csv("landing/claims_2026-08-22.csv", header=True, inferSchema=True)
    policies = spark.read.csv("landing/policies.csv", header=True, inferSchema=True)
    claims.createOrReplaceTempView("claims")
    policies.createOrReplaceTempView("policies")

    # 2) JOIN claims to their policies, then aggregate by product
    #    /*+ BROADCAST(p) */ broadcasts the small policies table (faster, no shuffle).
    metrics = spark.sql("""
        SELECT /*+ BROADCAST(p) */
            p.product_type,
            count(*)                      AS claim_count,
            round(sum(c.claim_amount), 2) AS total_claimed,
            round(avg(c.claim_amount), 2) AS avg_claim
        FROM claims c
        JOIN policies p ON c.policy_id = p.policy_id
        GROUP BY p.product_type
        ORDER BY total_claimed DESC
    """)
    metrics.show(truncate=False)

    # Show the execution plan — look for BroadcastHashJoin (proof of the optimization).
    metrics.explain()

    # 3) Write the result as Parquet.
    metrics.write.mode("overwrite").parquet("data/claims_by_product")
    print("Wrote claim metrics by product line to data/claims_by_product/ (Parquet)")

    spark.stop()


if __name__ == "__main__":
    main()