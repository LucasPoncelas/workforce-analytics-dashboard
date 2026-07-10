-- ============================================================
-- Workforce Analytics
-- File: 01_workforce_analysis.sql
-- Description:
-- SQL queries for workforce and employment analysis.
-- ============================================================

USE test_db;

-- ============================================================
-- 1. Total number of employees
-- ============================================================

SELECT COUNT(*) AS total_employees
FROM users;


-- ============================================================
-- 2. Employees by country
-- ============================================================

SELECT
    a.country,
    COUNT(*) AS employees
FROM users u
JOIN addresses a
    ON u.user_id = a.user_id
GROUP BY a.country
ORDER BY employees DESC;


-- ============================================================
-- 3. Average salary by job title
-- ============================================================

SELECT
    e.job_title,
    ROUND(AVG(e.salary), 2) AS average_salary
FROM employment e
GROUP BY e.job_title
ORDER BY average_salary DESC;


-- ============================================================
-- 4. Average salary by education level
-- ============================================================

SELECT
    ed.education_level,
    ROUND(AVG(e.salary), 2) AS average_salary
FROM employment e
JOIN education ed
    ON e.user_id = ed.user_id
GROUP BY ed.education_level
ORDER BY average_salary DESC;


-- ============================================================
-- 5. Employment status distribution
-- ============================================================

SELECT
    employment_status,
    COUNT(*) AS employees
FROM employment
GROUP BY employment_status
ORDER BY employees DESC;


-- ============================================================
-- 6. Job satisfaction distribution
-- ============================================================

SELECT
    job_satisfaction,
    COUNT(*) AS employees
FROM employment
GROUP BY job_satisfaction
ORDER BY employees DESC;


-- ============================================================
-- 7. Average years of experience by profession
-- ============================================================

SELECT
    job_title,
    ROUND(AVG(years_experience),1) AS average_experience
FROM employment
GROUP BY job_title
ORDER BY average_experience DESC;


-- ============================================================
-- 8. Average work-from-home days by profession
-- ============================================================

SELECT
    job_title,
    ROUND(AVG(work_from_home_days),1) AS average_remote_days
FROM employment
GROUP BY job_title
ORDER BY average_remote_days DESC;


-- ============================================================
-- 9. Top 10 highest salaries
-- ============================================================

SELECT
    CONCAT(u.name,' ',u.surname) AS employee,
    e.job_title,
    e.company_name,
    e.salary
FROM users u
JOIN employment e
    ON u.user_id = e.user_id
ORDER BY e.salary DESC
LIMIT 10;


-- ============================================================
-- 10. Company size distribution
-- ============================================================

SELECT
    company_size,
    COUNT(*) AS employees
FROM employment
GROUP BY company_size
ORDER BY employees DESC;


-- ============================================================
-- 11. Average commute time by employment status
-- ============================================================

SELECT
    employment_status,
    ROUND(AVG(commute_time_minutes),1) AS average_commute
FROM employment
GROUP BY employment_status
ORDER BY average_commute;


-- ============================================================
-- 12. Vacation days by job title
-- ============================================================

SELECT
    job_title,
    ROUND(AVG(vacation_days),1) AS average_vacation_days
FROM employment
GROUP BY job_title
ORDER BY average_vacation_days DESC;