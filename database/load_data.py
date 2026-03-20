import pandas as pd
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine,text
# create_engine : This is how you connect Python to your database.
# text:This is used when you want to write raw SQL queries safely.

load_dotenv()

DB_URL=(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

def load_jobs(df,engine):
    """load jobs into jobs table"""
    jobs_df=df[[
        'title', 'company', 'location',
        'category', 'seniority', 'job_type',
        'job_url', 'scraped_date'
    ]].copy()

    # Inner brackets → a list of column names
    # Outer brackets → selecting from the DataFrame

    jobs_df['scraped_date']=pd.to_datetime(
        jobs_df['scraped_date'],errors='coerce' #errors='coerce' → invalid values become NaT (null)
    ).dt.date   #.dt.date → removes time, keeps only date

    jobs_df.to_sql(
        'jobs', 
        'engine',
        if_exists='append',
        index=False
    )
    print(f"Loaded {len(jobs_df)} jobs into jobs table")

def verify_load(engine):
    """Quick check that data loaded correctly"""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM jobs"))
        count = result.fetchone()[0]
        print(f"Total jobs in database: {count}")

        print("\nSample data:")
        result = conn.execute(text(
            "SELECT title, company, location, category FROM jobs LIMIT 5"
        ))
        for row in result:
            print(f"  {row[0]} | {row[1]} | {row[2]} | {row[3]}")

if __name__ == "__main__":
    print("Connecting to database...")
    engine = create_engine(DB_URL)

    print("Loading clean data...")
    df = pd.read_csv("data/processed/kumarijob_clean.csv")
    print(f"Read {len(df)} rows from CSV")

    load_jobs(df, engine)
    verify_load(engine)

    print("\nDone!")