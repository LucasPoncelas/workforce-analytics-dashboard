-- ============================================================
-- Workforce Analytics
-- File: 03_health_analysis.sql
-- Description:
-- SQL queries for health analysis.
-- ============================================================

USE test_db;

-- ============================================================
-- 1. BMI category distribution
-- ============================================================

SELECT
    bmi_category,
    COUNT(*) AS employees
FROM health
GROUP BY bmi_category;


-- ============================================================
-- 2. Average BMI
-- ============================================================

SELECT
    ROUND(AVG(bmi),1) AS average_bmi
FROM health;


-- ============================================================
-- 3. Average sleep hours
-- ============================================================

SELECT
    ROUND(AVG(sleep_hours),1) AS average_sleep
FROM health;


-- ============================================================
-- 4. Weekly exercise hours
-- ============================================================

SELECT
    ROUND(AVG(weekly_exercise_hours),1) AS average_exercise
FROM health;


-- ============================================================
-- 5. Smoking habits
-- ============================================================

SELECT
    is_smoker,
    COUNT(*) AS employees
FROM health
GROUP BY is_smoker;


-- ============================================================
-- 6. Insurance coverage
-- ============================================================

SELECT
    has_insurance,
    COUNT(*) AS employees
FROM health
GROUP BY has_insurance;


-- ============================================================
-- 7. Alcohol consumption
-- ============================================================

SELECT
    alcohol_consumption,
    COUNT(*) AS employees
FROM health
GROUP BY alcohol_consumption
ORDER BY employees DESC;


-- ============================================================
-- 8. Average BMI by profession
-- ============================================================

SELECT
    e.job_title,
    ROUND(AVG(h.bmi),1) AS average_bmi
FROM health h
JOIN employment e
ON h.user_id = e.user_id
GROUP BY e.job_title
ORDER BY average_bmi DESC;


-- ============================================================
-- 9. Lifestyle by country
-- ============================================================

SELECT
    a.country,
    ROUND(AVG(h.sleep_hours),1) AS average_sleep,
    ROUND(AVG(h.weekly_exercise_hours),1) AS average_exercise
FROM health h
JOIN addresses a
ON h.user_id = a.user_id
GROUP BY a.country;


-- ============================================================
-- 10. Average BMI by education level
-- ============================================================

SELECT
    ed.education_level,
    ROUND(AVG(h.bmi),1) AS average_bmi
FROM health h
JOIN education ed
ON h.user_id = ed.user_id
GROUP BY ed.education_level;