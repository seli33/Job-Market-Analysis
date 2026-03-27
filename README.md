# Nepal Job Market Analytics

An end-to-end **data engineering project** that collects, processes, and analyzes job postings from Nepali job boards using a structured ETL pipeline.

The system extracts raw job data from the web, transforms it into a clean and normalized format, loads it into a relational database, and generates insights through SQL and visualization tools.

---

## Project Overview

This project is designed to answer key questions about the Nepal job market:

* What are the most in-demand job roles?
* Which cities have the highest job concentration?
* Which companies are hiring the most?
* What seniority levels dominate the market?
* Which industries show growth trends?

---

## Architecture

```
Web Source (KumariJob)
        │
        ▼
[ Extract Layer ]
Requests + BeautifulSoup
        │
        ▼
Raw Data (CSV)
        │
        ▼
[ Transform Layer ]
Pandas + Regex (Data Cleaning & Normalization)
        │
        ▼
Processed Data (CSV)
        │
        ▼
[ Load Layer ]
SQLAlchemy → PostgreSQL
        │
        ▼
[ Analytics Layer ]
SQL Queries
        │
        ▼
[ Visualization Layer ]
Power BI Dashboard
```

---

## Key Features

* End-to-end ETL pipeline (Extract → Transform → Load)
* Modular project structure with clear separation of concerns
* Web scraping using BeautifulSoup and Requests
* Data cleaning and normalization using Pandas
* Relational database design using PostgreSQL
* Analytical querying using SQL
* Interactive dashboard using Power BI
* Environment-based configuration using `.env`

---

## Folder Structure

```
job-market-analysis/
│
├── data/
│   ├── raw/                    # Raw scraped data (gitignored)
│   └── processed/              # Cleaned datasets (gitignored)
│
├── scraper/                    # Extraction layer
│   ├── scrape_kumarijobs.py
│   ├── inspect_kumarijob.py
│   ├── inspect_category.py
│   └── verify_scraper.py
│
├── etl/                        # Transformation layer
│   ├── clean.py                # Production ETL script
│   └── etl_cleaning.ipynb      # Exploratory notebook
│
├── database/                   # Load layer
│   ├── schema.sql
│   └── load_data.py
│
├── analysis/                   # Analytics layer
│   └── queries.sql
│
├── dashboard/                  # Visualization layer
│   └── powerbi.pbix
│
├── pipeline/                   # Pipeline orchestration
│   └── main.py
│
├── notebooks/
│   └── explore.ipynb
│
├── config/
│   └── config.py
│
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

---

## Tech Stack

| Layer           | Tools                           |
| --------------- | ------------------------------- |
| Extraction      | Python, Requests, BeautifulSoup |
| Transformation  | Pandas, NumPy, Regex            |
| Database        | PostgreSQL                      |
| ORM / Connector | SQLAlchemy, psycopg2            |
| Analytics       | SQL                             |
| Visualization   | Power BI                        |
| Environment     | python-dotenv                   |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/job-market-analysis.git
cd job-market-analysis
```

### 2. Create virtual environment

```bash
python -m venv job_analysis
job_analysis\Scripts\activate      # Windows
source job_analysis/bin/activate   # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Update `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=job_market
DB_USER=postgres
DB_PASSWORD=your_password
```

---

## Database Setup

Create database:

```bash
psql -U postgres -c "CREATE DATABASE job_market;"
```

Run schema:

```bash
psql -U postgres -d job_market -f database/schema.sql
```

---

## Pipeline Execution

Run the full ETL pipeline:

```bash
python pipeline/main.py
```

Pipeline stages:

1. Extract job postings from KumariJob
2. Transform and clean raw data
3. Load structured data into PostgreSQL

---

## Data Model

### jobs

| Column       | Description               |
| ------------ | ------------------------- |
| job_id       | Primary key               |
| title        | Cleaned job title         |
| company      | Company name              |
| location     | Normalized city           |
| category     | Job category              |
| seniority    | Experience level          |
| job_type     | Remote / Hybrid / On-site |
| job_url      | Source URL                |
| scraped_date | Date collected            |

### skills

| Column     | Description |
| ---------- | ----------- |
| skill_id   | Primary key |
| skill_name | Skill name  |

### job_skills

| Column   | Description |
| -------- | ----------- |
| job_id   | FK → jobs   |
| skill_id | FK → skills |

---

## Sample Queries

```sql
-- Top job roles
SELECT title, COUNT(*) AS count
FROM jobs
GROUP BY title
ORDER BY count DESC
LIMIT 10;

-- Jobs by city
SELECT location, COUNT(*) AS count
FROM jobs
GROUP BY location
ORDER BY count DESC;

-- Top hiring companies
SELECT company, COUNT(*) AS openings
FROM jobs
GROUP BY company
ORDER BY openings DESC
LIMIT 10;
```

---

## Reliability & Engineering Practices

* Environment-based configuration using `.env`
* Modular pipeline design for maintainability
* Data cleaning and normalization rules
* Structured relational schema design
* Separation of extraction, transformation, and loading layers

---

## Data Source

KumariJob (kumarijob.com) — a major Nepali job board covering IT, finance, marketing, engineering, and more.

---

## Future Improvements

* Automate pipeline scheduling using Apache Airflow
* Add API-based data ingestion (REST/GraphQL)
* Implement incremental data loading
* Containerize using Docker
* Add data validation and monitoring
* Use LLMs for skill extraction and text processing

---

## Disclaimer

This project uses publicly available data for educational purposes only. Please respect website terms of service and implement rate limiting when scraping.
