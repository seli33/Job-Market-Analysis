import requests
import pandas as pd
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = os.getenv("RAPIDAPI_HOST")

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}

QUERIES = [
    "data analyst",
    "data engineer",
    "machine learning engineer",
    "python developer remote",
    "business analyst",
    "software engineer",
    "AI engineer remote",
    "NLP engineer",
    "remote data scientist",
    "junior data analyst",
]

def fetch_job(query,num_pages=5):
    all_jobs=[]
    for page in range(1,num_pages+1):
        print(f" Fetching page {page} for '{query}'")
        params = {
            "query":      query,       # search term e.g. "data analyst Nepal"
            "page":       str(page),   # which page of results
            "num_pages":  "1",         # how many pages per request
            "date_posted": "month",    # only jobs from last 30 days
        }

        try:
            response=requests.get(
                "https://jsearch.p.rapidapi.com/search",
                headers=HEADERS,
                params=params,
                timeout=15

            )
            if response.status_code == 200:
                data = response.json()
                jobs = data.get("data", [])
                print(f"   Status: {data.get('status')} | Jobs found: {len(jobs)}")
                all_jobs.extend(jobs)

            elif response.status_code == 401:
                print("   ERROR: Invalid API key — check your .env file")
                break

            elif response.status_code == 403:
                print("   ERROR: API key not subscribed to JSearch")
                break

            elif response.status_code == 429:
                print("   Rate limited — waiting 30 seconds")
                time.sleep(30)

            else:
                print(f"   ERROR: Status {response.status_code}")
                print(f"   Response: {response.text[:200]}") 

        except Exception as e:
            print(f"Error:{e}")

        time.sleep(2)  # wait 2 seconds between pages

    return all_jobs  # return everything collected
            
def parse_job(raw_jobs,query):
    records=[]
    for job in raw_jobs:
        qualifications=job.get("job_highlights",{}).get("Qualifications",[])
        benefits=job.get("job_benefits") or []
        benefits_str=", ".join(benefits) if benefits else "N/A"
        records.append({
            "title":     job.get("job_title"),
            "company":   job.get("employer_name"),
            "location":  job.get("job_city"),
            "country":   job.get("job_country"),
            "job_type":  job.get("job_employment_type"),
            "is_remote": job.get("job_is_remote"),
            "salary_min":job.get("job_min_salary"),
            "salary_max":job.get("job_max_salary"),
            "salary":job.get("job_salary"),
            "description":job.get("job_description"),
            "qualifications": " | ".join(qualifications[:5]),
            "benefits":  benefits_str,
            "posted_date":job.get("job_posted_at_datetime_utc"),
            "apply_url": job.get("job_apply_link"),
            "source":    "JSearch API",
            "scraped_at":datetime.now().strftime("%Y-%m-%d")
        })
    return records  # list of clean dictionaries

def scrape_all_queries():
    all_records = []
    seen_titles = set()  # set is like a list but no duplicates allowed

    for query in QUERIES:         # loop each search query
        print(f"Query: '{query}'")
        raw_jobs = fetch_job(query, num_pages=2)   # call API
        records  = parse_job(raw_jobs, query)       # clean results

        # Remove duplicates
        for record in records:
            # Create a unique key from title + company
            key = f"{record['title']}_{record['company']}"

            if key not in seen_titles:   # if we haven't seen this job
                seen_titles.add(key)     # mark it as seen
                all_records.append(record)  # add to final list

        time.sleep(3)  # pause between queries

    return all_records
if __name__ == "__main__":
    records = scrape_all_queries()  # run everything

    df = pd.DataFrame(records)      # convert list of dicts to DataFrame

    os.makedirs("data/raw", exist_ok=True)  # create folder if not exists

    # Create filename with today's date
    filename = f"data/raw/api_jobs_{datetime.now().strftime('%Y%m%d')}.csv"

    df.to_csv(filename, index=False)  # save to CSV

    print(f"Total unique jobs: {len(df)}")
    print(df[["title", "company", "location", "salary_min"]].head(10))