-- ============================================================
-- Workforce Analytics
-- File: 04_purchase_analysis.sql
-- Description:
-- SQL queries for purchase analysis.
-- ============================================================

USE test_db;

-- ============================================================
-- 1. Total purchases
-- ============================================================

SELECT COUNT(*) AS total_purchases
FROM purchases;


-- ============================================================
-- 2. Total purchase amount
-- ============================================================

SELECT
    ROUND(SUM(amount),2) AS total_sales
FROM purchases;


-- ============================================================
-- 3. Average purchase amount
-- ============================================================

SELECT
    ROUND(AVG(amount),2) AS average_purchase
FROM purchases;


-- ============================================================
-- 4. Purchases by category
-- ============================================================

SELECT
    category,
    COUNT(*) AS purchases,
    ROUND(SUM(amount),2) AS total_sales
FROM purchases
GROUP BY category
ORDER BY total_sales DESC;


-- ============================================================
-- 5. Payment methods
-- ============================================================

SELECT
    payment_method,
    COUNT(*) AS purchases
FROM purchases
GROUP BY payment_method;


-- ============================================================
-- 6. Top stores
-- ============================================================

SELECT
    store,
    COUNT(*) AS purchases,
    ROUND(SUM(amount),2) AS total_sales
FROM purchases
GROUP BY store
ORDER BY total_sales DESC
LIMIT 10;


-- ============================================================
-- 7. Purchases by country
-- ============================================================

SELECT
    a.country,
    ROUND(SUM(p.amount),2) AS total_sales
FROM purchases p
JOIN addresses a
ON p.user_id = a.user_id
GROUP BY a.country
ORDER BY total_sales DESC;


-- ============================================================
-- 8. Average purchase by profession
-- ============================================================

SELECT
    e.job_title,
    ROUND(AVG(p.amount),2) AS average_purchase
FROM purchases p
JOIN employment e
ON p.user_id = e.user_id
GROUP BY e.job_title
ORDER BY average_purchase DESC;


-- ============================================================
-- 9. Average purchase by education level
-- ============================================================

SELECT
    ed.education_level,
    ROUND(AVG(p.amount),2) AS average_purchase
FROM purchases p
JOIN education ed
ON p.user_id = ed.user_id
GROUP BY ed.education_level
ORDER BY average_purchase DESC;


-- ============================================================
-- 10. Monthly purchase trend
-- ============================================================

SELECT
    DATE_FORMAT(purchase_date,'%Y-%m') AS purchase_month,
    COUNT(*) AS purchases,
    ROUND(SUM(amount),2) AS total_sales
FROM purchases
GROUP BY purchase_month
ORDER BY purchase_month;