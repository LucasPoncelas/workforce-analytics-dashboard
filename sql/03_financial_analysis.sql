-- ============================================================
-- Workforce Analytics
-- File: 02_financial_analysis.sql
-- Description:
-- SQL queries for financial analysis.
-- ============================================================

USE test_db;

-- ============================================================
-- 1. Average savings
-- ============================================================

SELECT
    ROUND(AVG(savings),2) AS average_savings
FROM financial;


-- ============================================================
-- 2. Average debt amount
-- ============================================================

SELECT
    ROUND(AVG(debt_amount),2) AS average_debt
FROM financial;


-- ============================================================
-- 3. Average disposable income
-- ============================================================

SELECT
    ROUND(AVG(monthly_disposable_income),2) AS average_disposable_income
FROM financial;


-- ============================================================
-- 4. Credit score distribution
-- ============================================================

SELECT
    credit_score,
    COUNT(*) AS employees
FROM financial
GROUP BY credit_score
ORDER BY credit_score;


-- ============================================================
-- 5. Employees with mortgage
-- ============================================================

SELECT
    has_mortgage,
    COUNT(*) AS employees
FROM financial
GROUP BY has_mortgage;


-- ============================================================
-- 6. Average savings by education level
-- ============================================================

SELECT
    ed.education_level,
    ROUND(AVG(f.savings),2) AS average_savings
FROM financial f
JOIN education ed
ON f.user_id = ed.user_id
GROUP BY ed.education_level
ORDER BY average_savings DESC;


-- ============================================================
-- 7. Average salary vs disposable income
-- ============================================================

SELECT
    ROUND(AVG(e.salary),2) AS average_salary,
    ROUND(AVG(f.monthly_disposable_income),2) AS average_disposable_income
FROM employment e
JOIN financial f
ON e.user_id = f.user_id;


-- ============================================================
-- 8. Top 10 investment portfolios
-- ============================================================

SELECT
    CONCAT(u.name,' ',u.surname) AS employee,
    investment_portfolio_value
FROM financial f
JOIN users u
ON f.user_id = u.user_id
ORDER BY investment_portfolio_value DESC
LIMIT 10;


-- ============================================================
-- 9. Average housing cost by country
-- ============================================================

SELECT
    a.country,
    ROUND(AVG(f.housing_cost),2) AS average_housing_cost
FROM financial f
JOIN addresses a
ON f.user_id = a.user_id
GROUP BY a.country
ORDER BY average_housing_cost DESC;


-- ============================================================
-- 10. Financial overview by profession
-- ============================================================

SELECT
    e.job_title,
    ROUND(AVG(f.savings),2) AS avg_savings,
    ROUND(AVG(f.debt_amount),2) AS avg_debt,
    ROUND(AVG(f.monthly_disposable_income),2) AS avg_disposable_income
FROM financial f
JOIN employment e
ON f.user_id = e.user_id
GROUP BY e.job_title
ORDER BY avg_disposable_income DESC;