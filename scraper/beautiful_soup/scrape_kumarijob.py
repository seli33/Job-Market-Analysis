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
    "customer_service": "customer-service-jobs-in-nepal",
    "hospitality":      "hospitality-jobs-in-nepal",
    "education":        "education-jobs-in-nepal",
    "banking":          "banking-jobs-in-nepal",
    "hr":               "human-resource-jobs-in-nepal",
    "healthcare":       "health-medical-pharmaceuticals-jobs-in-nepal",
}


def scrape_job_detail(job_url):
    """
    Visit individual job page to get full description,
    salary and deadline — needed for ML extractor model
    """
    if job_url == "N/A":
        return {"description": "N/A", "deadline": "N/A", "salary": "N/A"}

    try:
        response = requests.get(
            job_url, headers=HEADERS, timeout=10
        )

        if response.status_code != 200:
            return {"description": "N/A", "deadline": "N/A", "salary": "N/A"}

        soup = BeautifulSoup(response.text, "html.parser")

        # Try multiple selectors for description
        # Different job pages may use different class names
        description = "N/A"
        for selector in [
            {"class": "job-description"},
            {"class": "description"},
            {"class": "job-details"},
            {"class": "job_description"},
            {"id": "job-description"},
        ]:
            found = soup.find("div", selector)
            if found:
                description = found.text.strip()
                break

        # Try to find deadline
        try:
            deadline = soup.find(
                "span", class_="deadline"
            ).text.strip()
        except:
            deadline = "N/A"

        # Try to find salary
        try:
            salary = soup.find(
                "span", class_="salary"
            ).text.strip()
        except:
            salary = "N/A"

        return {
            "description": description,
            "deadline":    deadline,
            "salary":      salary
        }

    except Exception as e:
        print(f"    Detail scrape failed: {e}")
        return {"description": "N/A", "deadline": "N/A", "salary": "N/A"}


def scrape_page(url, scrape_details=True):
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

        # ── TITLE ──────────────────────────────────────────
        title = h2.text.strip()

        # ── JOB URL ────────────────────────────────────────
        try:
            job_url = h2.find("a")["href"]
        except:
            job_url = "N/A"

        # ── NAVIGATE TO FULL CARD ──────────────────────────
        try:
            job_card = h2.find_parent("div", class_="job-card-body")
        except:
            job_card = None

        # ── COMPANY ────────────────────────────────────────
        try:
            company = job_card.find(
                "a", class_="link-route"
            ).text.strip()
        except:
            company = "N/A"

        # ── LOCATION ───────────────────────────────────────
        try:
            location = job_card.find(
                "span", class_="district-text"
            ).text.strip()
        except:
            location = "N/A"

        # ── DETAIL PAGE ────────────────────────────────────
        # Visit each job URL to get description, salary, deadline
        if scrape_details and job_url != "N/A":
            print(f"    Scraping detail: {title[:40]}...")
            detail = scrape_job_detail(job_url)
            # Polite delay between detail requests
            time.sleep(random.uniform(1, 2))
        else:
            detail = {
                "description": "N/A",
                "deadline":    "N/A",
                "salary":      "N/A"
            }

        jobs.append({
            "title":        title,
            "company":      company,
            "location":     location,
            "job_url":      job_url,
            "description":  detail["description"],
            "deadline":     detail["deadline"],
            "salary":       detail["salary"],
            "scraped_date": datetime.now().strftime("%Y-%m-%d")
        })

    return jobs


def scrape_category(name, slug, max_pages=10, scrape_details=True):
    all_jobs = []
    base_url  = f"https://www.kumarijob.com/jobs-in-nepal/{slug}"

    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}"
        print(f"  Page {page}: {url}")

        jobs = scrape_page(url, scrape_details=scrape_details)

        if not jobs:
            print(f"  No jobs found on page {page} - stopping category.")
            break

        all_jobs.extend(jobs)
        print(f"  Found {len(jobs)} jobs on page {page}")

        # Random delay between pages
        time.sleep(random.uniform(2, 4))

    return all_jobs


def scrape_all(max_pages=10, scrape_details=True):
    all_jobs = []

    for name, slug in CATEGORIES.items():
        print(f"\nScraping category: {name.upper()}")
        jobs = scrape_category(
            name, slug,
            max_pages=max_pages,
            scrape_details=scrape_details
        )

        # Tag each job with its category
        for job in jobs:
            job["category"] = name

        all_jobs.extend(jobs)
        print(f"  Total for {name}: {len(jobs)} jobs")

    # Convert to DataFrame
    df = pd.DataFrame(all_jobs)

    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates(subset=["title", "company"])
    after  = len(df)
    print(f"\nDuplicates removed: {before - after}")

    # Save to CSV
    os.makedirs("data/raw", exist_ok=True)
    filename = "data/raw/kumarijob_info.csv"
    df.to_csv(filename, index=False)
    print(f"Saved {after} jobs to {filename}")

    return df


if __name__ == "__main__":

    # Set scrape_details=False for a quick test run
    # Set scrape_details=True for full data with descriptions
    df = scrape_all(max_pages=10, scrape_details=True)

    print("\nSample output:")
    print(df[["title", "company", "location",
              "category", "salary"]].head(10))

    print("\nDescription sample:")
    sample = df[df["description"] != "N/A"]["description"].iloc[0]
    print(sample[:300])

    print(f"\nFinal stats:")
    print(f"Total jobs:              {len(df)}")
    print(f"Jobs with description:   {(df['description'] != 'N/A').sum()}")
    print(f"Jobs with salary:        {(df['salary'] != 'N/A').sum()}")
    print(f"Jobs with deadline:      {(df['deadline'] != 'N/A').sum()}")
    print(f"Categories: {df['category'].value_counts().to_dict()}")