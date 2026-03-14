#  Nepal Job Market Analytics

A end-to-end data engineering project that scrapes job postings from Nepali job boards, cleans and transforms the data, loads it into a PostgreSQL database, and generates insights about the local job market.

---

##  Project Goal

Answer real questions about the Nepal job market:

- What are the most in-demand job roles in Nepal?
- Which cities have the most job openings?
- Which companies are hiring the most?
- What seniority levels are most common?
- Which industries are growing?

---

## Architecture

```
Web Source (KumariJob)
        │
        ▼
  [ Scraper Layer ]          Python + BeautifulSoup
  scraper/scrape_kumarijobs.py
        │
        ▼ CSV (raw)
  [ ETL Layer ]              Python + Pandas + Regex
  etl/etl_cleaning.ipynb
        │
        ▼ CSV (clean)
  [ Database Layer ]         PostgreSQL
  database/schema.sql
  database/load_data.py
        │
        ▼
  [ Analytics Layer ]        SQL
  analysis/queries.sql
        │
        ▼
  [ Visualization Layer ]    Power BI
  dashboard/
```

---

##  Folder Structure

```
job-market-analysis/
│
├── data/
│   ├── raw/                    # Raw scraped CSVs (gitignored)
│   └── processed/              # Cleaned CSVs (gitignored)
│
├── scraper/
│   ├── inspect_kumarijob.py    # Inspect site HTML structure
│   ├── inspect_category.py     # Inspect category page structure
│   ├── verify_scraper.py       # Verify selectors work
│   └── scrape_kumarijobs.py    # Main scraper
│
├── etl/
│   ├── etl_cleaning.ipynb      # Full ETL cleaning notebook
│   └── explore.py              # EDA profiling script
│
├── database/
│   ├── schema.sql              # PostgreSQL table definitions
│   └── load_data.py            # Load clean CSV into database
│
├── analysis/
│   └── queries.sql             # Analytical SQL queries
│
├── dashboard/
│   └── powerbi.pbix            # Power BI dashboard
│
├── notebooks/
│   └── explore.ipynb           # Exploratory analysis notebook
│
├── .env                        # DB credentials (gitignored)
├── .env.example                # Credentials template (committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

##  Tech Stack

| Layer | Tool |
|---|---|
| Scraping | Python, Requests, BeautifulSoup |
| Data Cleaning | Python, Pandas, NumPy, Regex |
| Database | PostgreSQL, pgAdmin |
| DB Connector | SQLAlchemy, psycopg2 |
| Analytics | SQL |
| Visualization | Power BI |
| Environment | Python venv, python-dotenv |

---

##  Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/job-market-analysis.git
cd job-market-analysis
```

### 2. Create and activate virtual environment

```bash
python -m venv job_analysis
job_analysis\Scripts\activate      # Windows
source job_analysis/bin/activate   # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=job_market
DB_USER=postgres
DB_PASSWORD=your_password_here
```

### 5. Set up the database

Open pgAdmin, create a database called `job_market`, then run:

```bash
psql -U postgres -d job_market -f database/schema.sql
```

---

## ▶️ Running the Pipeline

### Step 1 — Scrape jobs

```bash
python scraper/scrape_kumarijobs.py
```

Scrapes 7 job categories from KumariJob.com and saves to `data/raw/`.

### Step 2 — Clean the data

Open `etl/etl_cleaning.ipynb` in VSCode and run all cells top to bottom.

Outputs clean CSV to `data/processed/kumarijob_clean.csv`.

### Step 3 — Load into database

```bash
python database/load_data.py
```

### Step 4 — Run analytics

Open pgAdmin and run queries from `analysis/queries.sql`.

---

## 📊 Data Schema

### jobs table

| Column | Type | Description |
|---|---|---|
| job_id | SERIAL PRIMARY KEY | Unique job ID |
| title | TEXT | Cleaned job title |
| company | TEXT | Company name |
| location | TEXT | Normalized city |
| category | TEXT | Job category |
| seniority | TEXT | Senior / Mid-Level / Junior |
| job_type | TEXT | Remote / Hybrid / On-site |
| job_url | TEXT | Link to original posting |
| scraped_date | DATE | Date scraped |

### skills table

| Column | Type | Description |
|---|---|---|
| skill_id | SERIAL PRIMARY KEY | Unique skill ID |
| skill_name | TEXT | e.g. Python, SQL, Excel |

### job_skills table

| Column | Type | Description |
|---|---|---|
| job_id | INTEGER | Foreign key → jobs |
| skill_id | INTEGER | Foreign key → skills |

---

## 🔍 Sample Analytics Queries

```sql
-- Most common job titles
SELECT title, COUNT(*) AS count
FROM jobs
GROUP BY title
ORDER BY count DESC
LIMIT 10;

-- Jobs per city
SELECT location, COUNT(*) AS count
FROM jobs
GROUP BY location
ORDER BY count DESC;

-- Jobs per category
SELECT category, COUNT(*) AS count
FROM jobs
GROUP BY category
ORDER BY count DESC;

-- Most hiring companies
SELECT company, COUNT(*) AS openings
FROM jobs
GROUP BY company
ORDER BY openings DESC
LIMIT 10;

-- Seniority distribution
SELECT seniority, COUNT(*) AS count
FROM jobs
GROUP BY seniority
ORDER BY count DESC;
```

---

## 🌐 Data Source

**KumariJob** (kumarijob.com) — one of Nepal's leading job boards covering categories including IT, accounting, marketing, engineering, digital marketing, content writing, and full stack development.

Categories scraped:
- IT & Telecommunication
- Accounting & Finance
- Sales & Marketing
- Digital Marketing
- Engineering
- Full Stack Development
- Content Writing

---

## 🗺️ Roadmap

- [x] Web scraper for KumariJob
- [x] ETL cleaning pipeline
- [ ] PostgreSQL database setup
- [ ] Load data into database
- [ ] SQL analytics queries
- [ ] Power BI dashboard
- [ ] Automated daily pipeline (Airflow)
- [ ] Skill extraction from job descriptions
- [ ] ML job role classifier

---

## 📋 Requirements

```
requests
beautifulsoup4
pandas
numpy
sqlalchemy
psycopg2-binary
python-dotenv
selenium
webdriver-manager
jupyter
```

Install all with:

```bash
pip install -r requirements.txt
```

---

## ⚠️ Disclaimer

This project scrapes publicly available job listing data for educational and research purposes only. Always respect a website's terms of service and robots.txt. Add delays between requests to avoid overloading servers.

---

