-- =====================================================
-- NEPAL JOB MARKET ANALYTICS
-- KumariJob Data | Scraped March 2026
-- =====================================================

-- =====================================================
-- 1. OVERVIEW
-- =====================================================

-- Total jobs in database
SELECT COUNT(*) AS total_jobs 
FROM jobs;

-- Jobs per category
SELECT 
category,
COUNT(*) AS total_jobs,
ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(),1) AS percentage
FROM jobs
GROUP BY category
ORDER BY total_jobs DESC
