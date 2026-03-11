import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

CATEGORIES = {
    "it":               "ittelecommunication-jobs-in-nepal",
    "accounting":       "accounting-and-finance-jobs-in-nepal",
    "marketing":        "marketing-sales-jobs-in-nepal",
    "engineering":      "engineering-jobs-in-nepal",
    "digital_marketing":"digital-marketing-jobs-in-nepal",
    "fullstack":        "full-stack-development-jobs-in-nepal",
    "content_writing":  "content-writer-content-editor-jobs-in-nepal",
}

def scrape_page(url):
    response = requests.get(url, headers=HEADERS, timeout=10)

    if response.status_code != 200:
        print(f"  Failed with status: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Each job title lives in h2.mb-0.fw-semibold
    job_titles = soup.find_all("h2", class_=["mb-0", "fw-semibold"])

    if not job_titles:
        return []

    jobs = []
    for h2 in job_titles:

        #  TITLE 
        title = h2.text.strip()

        #  JOB URL 
        # the <a> tag is directly inside the <h2>
        try:
            job_url = h2.find("a")["href"]
        except:
            job_url = "N/A"

        #  NAVIGATE TO FULL CARD 
        # h2 → parent: h2-text div
        # h2 → grandparent: job-card-body div
        # h2 → great grandparent: d-flex gap-3 div (full card)
        try:
            job_card = h2.find_parent("div", class_="job-card-body")
        except:
            job_card = None

        #  COMPANY 
        # inside job-card-body → views div → <a class="link-route">
        try:
            company = job_card.find("a", class_="link-route").text.strip()
        except:
            company = "N/A"

        #  LOCATION 
        # inside job-card-body → views div → <span class="district-text">
        try:
            location = job_card.find("span", class_="district-text").text.strip()
        except:
            location = "N/A"

        jobs.append({
            "title":      title,
            "company":    company,
            "location":   location,
            "job_url":    job_url,
            "scraped_date": datetime.now().strftime("%Y-%m-%d")
        })

    return jobs


def scrape_category(name, slug, max_pages=5):
    all_jobs = []
    base_url  = f"https://www.kumarijob.com/jobs-in-nepal/{slug}"

    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}"
        print(f"  Page {page}: {url}")

        jobs = scrape_page(url)

        if not jobs:
            print(f"  No jobs found on page {page} - stopping category.")
            break

        all_jobs.extend(jobs)
        print(f"  Found {len(jobs)} jobs on page {page}")

        # Random delay 
        time.sleep(random.uniform(2, 4))

    return all_jobs


def scrape_all(max_pages=3):
    all_jobs = []

    for name, slug in CATEGORIES.items():
        print(f"\nScraping category: {name.upper()}")
        jobs = scrape_category(name, slug, max_pages=max_pages)

        # Tag each job with its category
        for job in jobs:
            job["category"] = name

        all_jobs.extend(jobs)
        print(f"  Total for {name}: {len(jobs)} jobs")

    # Convert to DataFrame
    df = pd.DataFrame(all_jobs)

    # Remove duplicate job postings
    before = len(df)
    df = df.drop_duplicates(subset=["title", "company"])
    after  = len(df)
    print(f"\nDuplicates removed: {before - after}")

    # Save to CSV
    os.makedirs("data/raw", exist_ok=True)
    filename = f"data/raw/kumarijob_info.csv"
    df.to_csv(filename, index=False)
    print(f"Saved {after} jobs to {filename}")

    return df


if __name__ == "__main__":
    df = scrape_all(max_pages=3)
    print("\nSample output:")
    print(df[["title", "company", "location", "category"]].head(10))