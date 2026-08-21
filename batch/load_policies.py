import duckdb

SOURCE_CSV = "landing/policies.csv"
DB_PATH = "data/insurance.duckdb"

def load():
    con=duckdb.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS raw_policies(
        policy_id VARCHAR PRIMARY KEY,
        policyholder VARCHAR,
        state VARCHAR,
        product_type VARCHAR,
        annual_premium DOUBLE,
        start_date DATE,
        status VARCHAR,
        loaded_at TIMESTAMP
        )       
    """)
    before = con.execute("SELECT count(*) FROM raw_policies").fetchone()[0]
 
    con.execute(f"""
          INSERT INTO raw_policies
          SELECT *, now() AS loaded_at
          FROM read_csv_auto('{SOURCE_CSV}')
          ON CONFLICT (policy_id) DO NOTHING
      """)
  
    after = con.execute("SELECT count(*) FROM raw_policies").fetchone()[0]
    con.close()
    print(f"  raw_policies: added {after - before} new policies")


if __name__ == "__main__":
    load()
