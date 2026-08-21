import duckdb  # the library that lets Python talk to a DuckDB database
  
SOURCE_CSV = "landing/claims_2026-08-23.csv"
DB_PATH = "data/insurance.duckdb"
  

def load():
      con = duckdb.connect(DB_PATH)
      con.execute("""
          CREATE TABLE IF NOT EXISTS raw_claims (
              claim_id     VARCHAR PRIMARY KEY,
              policy_id    VARCHAR,
              claim_date   DATE,
              claim_type   VARCHAR,
              claim_amount DOUBLE,
              status       VARCHAR,
              state        VARCHAR,
              loaded_at    TIMESTAMP
          )
      """)

      before = con.execute("SELECT count(*) FROM raw_claims").fetchone()[0]
      rows_in_file = con.execute(
          f"SELECT count(*) FROM read_csv_auto('{SOURCE_CSV}')"
      ).fetchone()[0]
  
      con.execute(f"""
          INSERT INTO raw_claims
          SELECT *, now() AS loaded_at
          FROM read_csv_auto('{SOURCE_CSV}')
          ON CONFLICT (claim_id) DO NOTHING
      """)
  
      after = con.execute("SELECT count(*) FROM raw_claims").fetchone()[0]
      added = after - before
      con.close()
      print(f"  {SOURCE_CSV}: added {added} new, skipped {rows_in_file - added} already-seen")


def report():
      con = duckdb.connect(DB_PATH)
      total = con.execute("SELECT count(*) FROM raw_claims").fetchone()[0]
      print(f"Total claims now in table: {total}")

      print("Claims by status:")
      for status, n in con.execute("""
          SELECT status, count(*) FROM raw_claims GROUP BY status ORDER BY count(*) DESC
      """).fetchall():
          print(f"  {status:10} {n}")
      con.close()


if __name__ == "__main__":
      load()
      report()