import duckdb # the library that lets Python talk to a DuckDB database

# The source file that "landed" from the claims system, and where our DB will live
SOURCE_CSV = "landing/claims_2026-08-22.csv"
DB_PATH = "data/insurance.duckdb"

def load(): 
      """Read the claims CSV and load it into a raw_claims table."""
      con = duckdb.connect(DB_PATH)          # open (or create) the database file
      con.execute(f"""
          CREATE OR REPLACE TABLE raw_claims AS
          SELECT * FROM read_csv_auto('{SOURCE_CSV}')
      """)
      con.close()
      print(f"Loaded {SOURCE_CSV} into raw_claims")

 
def report():
      """Run a couple of SQL queries to prove it worked."""
      con = duckdb.connect(DB_PATH)
      total = con.execute("SELECT count(*) FROM raw_claims").fetchone()[0]
      print(f"Total claims loaded: {total}")

      print("Claims by status:")
      for status, n in con.execute("""
          SELECT status, count(*) FROM raw_claims GROUP BY status ORDER BY count(*) DESC
      """).fetchall():
          print(f"  {status:10} {n}")
      con.close()


if __name__ == "__main__":
      load()
      report()