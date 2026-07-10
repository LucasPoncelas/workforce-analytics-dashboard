import random
import traceback
import mysql.connector

from config import DB_CONFIG
from generators import generate_relational_person, random_purchase_history

TABLES = {
            'users': """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(50),
                    surname VARCHAR(50),
                    email VARCHAR(100),
                    birth_date DATE,
                    nationality VARCHAR(100),
                    marital_status VARCHAR(20),
                    sex VARCHAR(15),
                    height INT,
                    weight INT,
                    phone VARCHAR(20)
                )
            """,
            
            'addresses': """
                CREATE TABLE IF NOT EXISTS addresses (
                    address_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    country VARCHAR(100),
                    city VARCHAR(100),
                    state VARCHAR(100),
                    zip_code VARCHAR(20),
                    latitude DECIMAL(10, 8),
                    longitude DECIMAL(11, 8),
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            """,
            
            'employment': """
                CREATE TABLE IF NOT EXISTS employment (
                    employment_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    job_title VARCHAR(50),
                    salary DECIMAL(10,2),
                    salary_currency VARCHAR(3) DEFAULT 'USD',
                    employment_status ENUM('Full-time', 'Part-time', 'Contract', 'Freelance', 'Unemployed'),
                    company_name VARCHAR(100),
                    company_size VARCHAR(50),
                    years_experience INT,
                    job_satisfaction ENUM('Very Satisfied', 'Satisfied', 'Neutral', 'Unsatisfied', 'Very Unsatisfied'),
                    work_from_home_days INT,
                    commute_time_minutes INT,
                    vacation_days INT,
                    start_date DATE,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            """,

            'education': """
                CREATE TABLE IF NOT EXISTS education (
                    education_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    education_level VARCHAR(30),
                    field_of_study VARCHAR(100),
                    university VARCHAR(200),
                    graduation_year INT,
                    student_debt DECIMAL(10,2),
                    gpa DECIMAL(3,2),
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            """,

            'health': """
                CREATE TABLE IF NOT EXISTS health (
                    health_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    blood_type VARCHAR(5),
                    has_insurance ENUM('Yes', 'No'),
                    is_smoker ENUM('Yes', 'No'),
                    last_medical_check DATE,
                    bmi DECIMAL(4,1),
                    bmi_category VARCHAR(20),
                    weekly_exercise_hours INT,
                    alcohol_consumption ENUM('None', 'Low', 'Moderate', 'High'),
                    diet_type VARCHAR(50),
                    sleep_hours DECIMAL(3,1),
                    chronic_conditions TEXT,
                    allergies TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            """,

            'family': """ 
                CREATE TABLE IF NOT EXISTS family (
                    family_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    number_of_children INT,
                    dependents INT,
                    living_with_parents ENUM('Yes', 'No'),
                    household_size INT,
                    spouse_employed ENUM('Yes', 'No', 'Not Married'),
                    annual_household_income DECIMAL(12,2),
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            """,

            'financial': """
                CREATE TABLE IF NOT EXISTS financial (
                    finance_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    credit_score INT,
                    housing_cost DECIMAL(10,2),
                    food_expenses DECIMAL(10,2),
                    transportation_cost DECIMAL(10,2),
                    debt_amount DECIMAL(10,2),
                    savings DECIMAL(10,2),
                    investment_portfolio_value DECIMAL(12,2),
                    monthly_disposable_income DECIMAL(10,2),
                    has_mortgage ENUM('Yes', 'No'),
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            """,

            'purchases': """
                CREATE TABLE IF NOT EXISTS purchases (
                    purchase_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    purchase_date DATE,
                    amount DECIMAL(10,2),
                    category ENUM('Electronics', 'Clothing', 'Food', 'Entertainment', 'Travel', 'Health', 'Other'),
                    payment_method ENUM('Credit Card', 'Debit Card', 'Cash', 'Digital Wallet'),
                    store VARCHAR(100),
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            """
        }

def get_connection():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    return connection, cursor

def create_tables(cursor, connection):

    for table_name, sql in TABLES.items():
        cursor.execute(sql)

    connection.commit()

def drop_tables(cursor, connection):

    tables = [
        "purchases",
        "financial",
        "family",
        "health",
        "education",
        "employment",
        "addresses",
        "users"
    ]

    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")

    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

    connection.commit()
    
# Enter data into all related tables
def insert_relational_data(cursor, connection, num_records):
    total_purchases = 0
    for i in range(num_records):
        try:
            #Generate all the info
            all_data = generate_relational_person()
            
            #Insert info into USERS table and get ID
            user_data = all_data['users']
            cursor.execute("""
                INSERT INTO users 
                (name, surname, email, birth_date, nationality, marital_status, 
                 sex, height, weight, phone)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                user_data['name'], user_data['surname'], user_data['email'],
                user_data['birth_date'], user_data['nationality'], user_data['marital_status'],
                user_data['sex'], user_data['height'], user_data['weight'],
                user_data['phone']
            ))
            
            user_id = cursor.lastrowid
            
            #Insertar datos en addresses
            address_data = all_data['addresses']
            cursor.execute("""
                INSERT INTO addresses 
                (user_id, country, city, state, zip_code, 
                 latitude, longitude)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id, address_data['country'], address_data['city'],
                address_data['state'], address_data['zip_code'],
                address_data['latitude'],address_data['longitude']
            ))
            
            #Insert info into family
            family_data = all_data['family']
            cursor.execute("""
                INSERT INTO family 
                (user_id, number_of_children, dependents, living_with_parents,
                 household_size, spouse_employed, annual_household_income)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id, family_data['number_of_children'], 
                family_data['dependents'], family_data['living_with_parents'],
                family_data['household_size'], family_data['spouse_employed'],
                family_data['annual_household_income']
            ))
            
            #Insert info into education
            education_data = all_data['education']
            cursor.execute("""
                INSERT INTO education 
                (user_id, education_level, field_of_study, university,
                 graduation_year, student_debt, gpa)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id, education_data['education_level'],
                education_data['field_of_study'], education_data['university'],
                education_data['graduation_year'], education_data['student_debt'],
                education_data['gpa']
            ))
            
            #Insert info into employment
            employment_data = all_data['employment']
            cursor.execute("""
                INSERT INTO employment 
                (user_id, job_title, salary, employment_status, company_name,
                 company_size, years_experience, job_satisfaction, work_from_home_days,
                 commute_time_minutes, vacation_days, start_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id, employment_data['job_title'], employment_data['salary'],
                employment_data['employment_status'], employment_data['company_name'],
                employment_data['company_size'], employment_data['years_experience'],
                employment_data['job_satisfaction'], employment_data['work_from_home_days'],
                employment_data['commute_time_minutes'], employment_data['vacation_days'],
                employment_data['start_date']
            ))
            
            #Insert info into health
            health_data = all_data['health']
            cursor.execute("""
                INSERT INTO health 
                (user_id, blood_type, has_insurance, is_smoker, last_medical_check,
                 bmi, bmi_category, weekly_exercise_hours, alcohol_consumption,
                 diet_type, sleep_hours, chronic_conditions, allergies)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id, health_data['blood_type'], health_data['has_insurance'],
                health_data['is_smoker'], health_data['last_medical_check'],
                health_data['bmi'], health_data['bmi_category'],
                health_data['weekly_exercise_hours'], health_data['alcohol_consumption'],
                health_data['diet_type'], health_data['sleep_hours'],
                health_data['chronic_conditions'], health_data['allergies']
            ))
            
            #Insert info into financial
            financial_data = all_data['financial']
            cursor.execute("""
                INSERT INTO financial 
                (user_id, credit_score, housing_cost, food_expenses,
                 transportation_cost, debt_amount, savings,
                 investment_portfolio_value, monthly_disposable_income, has_mortgage)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id, financial_data['credit_score'],
                financial_data['housing_cost'], financial_data['food_expenses'],
                financial_data['transportation_cost'], financial_data['debt_amount'],
                financial_data['savings'], financial_data['investment_portfolio_value'],
                financial_data['monthly_disposable_income'], financial_data['has_mortgage']
            ))

            num_purchases = random.randint(1, 15)
            purchases_data = random_purchase_history(user_id, num_purchases)   
            #Insert info into purchases (multiple per user)              
            for purchase in purchases_data:
                cursor.execute("""
                    INSERT INTO purchases 
                    (user_id, purchase_date, amount, category, payment_method, store)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    purchase['user_id'], purchase['purchase_date'], purchase['amount'],
                    purchase['category'], purchase['payment_method'], purchase['store']
                ))
                total_purchases += 1 
                     
        except Exception:
            print(f"\nError inserting record {i + 1}")
            traceback.print_exc()
            connection.rollback()
            raise
    connection.commit()
    return total_purchases

def close_connection(connection, cursor):
    cursor.close()
    connection.close()


