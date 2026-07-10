import os

import pandas as pd

from sqlalchemy import create_engine
from config import DB_CONFIG

def export_to_csv():
    """
    Export the relational workforce dataset from MySQL to a CSV file.
    """

    query = """
        SELECT
            u.user_id,
            u.name,
            u.surname,
            u.email,
            u.birth_date,
            u.nationality,
            u.marital_status,
            u.sex,
            u.height,
            u.weight,
            u.phone,

            a.country,
            a.city,
            a.state,
            a.zip_code,
            a.latitude,
            a.longitude,

            e.job_title,
            e.salary,
            e.salary_currency,
            e.employment_status,
            e.company_name,
            e.company_size,
            e.years_experience,
            e.job_satisfaction,
            e.work_from_home_days,
            e.commute_time_minutes,
            e.vacation_days,
            e.start_date,

            ed.education_level,
            ed.field_of_study,
            ed.university,
            ed.graduation_year,
            ed.student_debt,
            ed.gpa,

            h.blood_type,
            h.has_insurance,
            h.is_smoker,
            h.last_medical_check,
            h.bmi,
            h.bmi_category,
            h.weekly_exercise_hours,
            h.alcohol_consumption,
            h.diet_type,
            h.sleep_hours,
            h.chronic_conditions,
            h.allergies,

            f.number_of_children,
            f.dependents,
            f.living_with_parents,
            f.household_size,
            f.spouse_employed,
            f.annual_household_income,

            fi.credit_score,
            fi.housing_cost,
            fi.food_expenses,
            fi.transportation_cost,
            fi.debt_amount,
            fi.savings,
            fi.investment_portfolio_value,
            fi.monthly_disposable_income,
            fi.has_mortgage

        FROM users u

        LEFT JOIN addresses a
            ON u.user_id = a.user_id

        LEFT JOIN employment e
            ON u.user_id = e.user_id

        LEFT JOIN education ed
            ON u.user_id = ed.user_id

        LEFT JOIN health h
            ON u.user_id = h.user_id

        LEFT JOIN family f
            ON u.user_id = f.user_id

        LEFT JOIN financial fi
            ON u.user_id = fi.user_id
    """

    engine = create_engine(
        "mysql+mysqlconnector://"
        f"{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
        f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/"
        f"{DB_CONFIG['database']}"
    )

    df = pd.read_sql(query, engine)

    engine.dispose()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    dataset_dir = os.path.join(base_dir, "dataset")
    os.makedirs(dataset_dir, exist_ok=True)

    output_path = os.path.join(
        dataset_dir,
        "workforce_dataset.csv"
    )

    df.to_csv(output_path, index=False)

    print(f"CSV exported successfully: {output_path}")
