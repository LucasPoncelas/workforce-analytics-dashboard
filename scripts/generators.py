# Standard Library
import random
import warnings
from datetime import datetime, timedelta

# Third-party
import pandas as pd
import pgeocode
from faker import Faker
from mimesis import Person
from mimesis.enums import Gender

# Local
from constants import (
    COUNTRY_TO_ISO,
    COUNTRY_TO_MIMESIS_LOCALE,
    JOB_BY_EDUCATION,
    JOB_COMPANIES,
    JOB_SALARY_MULTIPLIER,
)

fake_generic = Faker()

#Generate nationality    
def random_nationality():
    # Choose between the principal countries
    return random.choice(list(COUNTRY_TO_MIMESIS_LOCALE.keys()))

#Generate sex
def random_sex():
    return random.choice(['Male', 'Female'])


#Generate date of birth
def random_date(start_year=1965, end_year=2005):
    #Generate a valid random date within the specified years
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    
    if month == 2:  # Febrero
        day = random.randint(1, 28)  #(non-leap year)
    elif month in [4, 6, 9, 11]:  # Month with 30 days
        day = random.randint(1, 30)
    else:  # Month with 31 days
        day = random.randint(1, 31)
    
    return datetime(year, month, day).strftime('%Y-%m-%d')

#Generate names based on gender and nationality
def get_culturally_appropriate_name(gender, nationality):
    locale = COUNTRY_TO_MIMESIS_LOCALE.get(nationality, 'en')
    
    try:
        person_gen = Person(locale=locale)
        gender_enum = Gender.MALE if gender == 'Male' else Gender.FEMALE
        return person_gen.first_name(gender=gender_enum)
    except:
        try:
            # Create a Faker instance with the locale
            fake = Faker(locale)
            if gender == 'Male':
                return fake.first_name_male()
            else:
                return fake.first_name_female()
        except:
            # If the locale isn't valid for Faker, use the generic one
            if gender == 'Male':
                return fake_generic.first_name_male()
            else:
                return fake_generic.first_name_female()

#Generate a last name consistent with the nationality using Mimesis
def get_culturally_appropriate_surname(nationality):
    locale = COUNTRY_TO_MIMESIS_LOCALE.get(nationality, 'en')
    
    try:
        person_gen = Person(locale=locale)
        return person_gen.last_name()
    except:
        try:
            fake = Faker(locale)
            return fake.last_name()
        except:
            return fake_generic.last_name()    

#Generate salary
def random_salary(experience, education, job_title):
    base_salary = {
        'No degree':1200,
        'High School':1600,
        'Technical':1900,
        'Bachelor':2200,
        'Master':2800,
        'PhD':3500
    }
    base = base_salary.get(education,1500)
    salary = base + (experience * random.randint(80,150)    )
    salary *= JOB_SALARY_MULTIPLIER.get(job_title,1)
    return round(salary)

#Generate employment date
def random_employment_data(age, education):

    # Typical workforce entry age based on education level
    education_start_age = {
        'No degree': 18,
        'High School': 18,
        'Technical': 20,
        'Bachelor': 22,
        'Master': 24,
        'PhD': 28
    }
    start_work_age = education_start_age.get(education, 18)
    max_experience = min(45,max(0, age - start_work_age))
    experience_years = random.randint(
        max(0, max_experience - 5),
        max_experience
    )
    job_title = random.choice(JOB_BY_EDUCATION.get(education,list(JOB_COMPANIES.keys())))
    company_name, company_size = random.choice(
        list(JOB_COMPANIES[job_title].items())
    )
    work_from_home_days = random.randint(0, 5)
    commute_time_minutes = random.randint(0, 120)

    if experience_years <= 5:
        vacation_days = random.randint(15, 21)
    elif experience_years <= 15:
        vacation_days = random.randint(22, 30)
    else:
        vacation_days = random.randint(31, 35)  

    salary = random_salary(experience_years,education,job_title)

    satisfaction_score = 0

    if salary <= 2000:
        satisfaction_score -= 2
    elif salary <= 3000:
        satisfaction_score -= 1
    elif salary <= 4500:
        satisfaction_score += 1
    else:
        satisfaction_score += 2

    if commute_time_minutes >= 90:
        satisfaction_score -= 2
    elif commute_time_minutes >= 45:
        satisfaction_score -= 1   

    if work_from_home_days >= 4:
        satisfaction_score += 2
    elif work_from_home_days >= 2:
        satisfaction_score += 1

    if satisfaction_score <= -2:
        job_satisfaction = "Very Unsatisfied"
    elif satisfaction_score == -1:
        job_satisfaction = "Unsatisfied"
    elif satisfaction_score == 0:
        job_satisfaction = "Neutral"
    elif satisfaction_score <= 2:
        job_satisfaction = "Satisfied"
    else:
        job_satisfaction = "Very Satisfied"

    return {
        'job_title': job_title,
        'salary': salary,
        'employment_status': random.choices(['Full-time','Part-time','Contract','Freelance'],weights=[75,10,10,5],k=1)[0],
        'company_name': company_name,
        'company_size': company_size,
        'years_experience': experience_years,
        'job_satisfaction': job_satisfaction,
        'work_from_home_days': work_from_home_days,
        'commute_time_minutes': commute_time_minutes,
        'vacation_days': vacation_days,
        'start_date': (datetime.now() - timedelta(days=experience_years*365)).strftime('%Y-%m-%d')
    }

#Generate marital status
def random_marital_status():
    statuses = ['Single', 'Married', 'Divorced', 'Widowed', 'Separated']
    return random.choice(statuses)

#Generate family data
def random_family_data(age, marital_status,salary):

    household_size = 1
    dependents = 0

    if age < 22 and random.random() < 0.7:
        living_with_parents = "Yes"
        household_size += 2
    else:
        living_with_parents ='No'

    if age < 22:
        children = 0
    elif age < 35:
        children = random.randint(0,2)
        household_size += children
        dependents += children
    elif marital_status in ['Married','Widowed']:
        children = random.randint(0,4)
        dependents += children 
        household_size += children       
    else:
        children = random.randint(0,2)
        household_size += children
        dependents += children

    if marital_status in ['Married','Separated']:
        spouse_employed = "Yes" if random.random() < 0.75 else "No"
        household_size += 1
    else:
        spouse_employed = "Not Married"

    if spouse_employed == "Yes":
        annual_household_income = salary * random.uniform(1.7,2.2) * 12
    else:
        annual_household_income = salary * random.uniform(0.9,1.1) * 12

    return {
        'number_of_children': children,
        'dependents': dependents,
        'living_with_parents': living_with_parents,
        'household_size': household_size,
        'spouse_employed': spouse_employed,
        'annual_household_income': round(annual_household_income,2)
    }

#Generate education level
def random_education():
    levels = ['High School', 'Bachelor', 'Master', 'PhD', 'Technical',"No degree"]
    return random.choice(levels)

#Generate education data
def random_education_data(education_level, current_year, job_title, age):
    universities = {
        'High School': ['Local High School', 'Technical High School', 'Private High School'],
        'Bachelor': ['Harvard', 'Stanford', 'UNAM', 'USP', 'University of Tokyo', 'Sorbonne'],
        'Master': ['MIT', 'Oxford', 'Cambridge', 'ETH Zurich', 'University of Melbourne'],
        'PhD': ['Caltech', 'Princeton', 'Yale', 'University of Chicago', 'Imperial College'],
        'Technical': ['Technical Institute', 'Vocational School', 'Community College'],
        'No degree': [None]
    }
    
    fields = {
        'Developer':'Computer Science',
        'Engineer':'Engineering',
        'Doctor':'Medicine',
        'Scientist':'Science',
        'Teacher':'Education',
        'Architect':'Architecture',
        'Designer':'Design',
        'Chef':'Culinary Arts',
        'Artist':'Arts',
    }

    graduation_age = {
        'High School':18,
        'Technical':20,
        'Bachelor':22,
        'Master':24,
        'PhD':28
    }

    if education_level == "No degree":
        fields_study = None
    else:
        fields_study = fields.get(job_title)

    if education_level in graduation_age:
        graduation_year = current_year - (age - graduation_age[education_level])
    else:
        graduation_year = None        
    
    if education_level == 'Bachelor':
        student_debt = round(random.uniform(0, 25000),2)
        gpa = round(random.uniform(2.3, 4.0), 2)
    elif education_level == 'Master':
        student_debt = round(random.uniform(10000, 45000),2)
        gpa = round(random.uniform(2.8, 4.0), 2)        
    elif education_level == 'PhD':
        student_debt = round(random.uniform(20000, 70000),2)
        gpa = round(random.uniform(3.2, 4.0), 2)
    elif education_level == "High School": 
        student_debt = 0
        gpa = round(random.uniform(2.0, 4.0), 2)
    else: 
        student_debt = 0
        gpa = None

    if education_level == "No degree":
        university = None
    else:
        university = random.choice(universities[education_level])

    return {
        'education_level': education_level,
        'field_of_study': fields_study,
        'university': university,
        'graduation_year': graduation_year,
        'student_debt': student_debt,
        'gpa': gpa
    }

#Generate health data
def random_health_data(age, weight, height):
    bmi = weight / ((height/100) ** 2)
    is_smoker = "Yes" if random.random() < 0.25 else "No"
    has_insurance = "Yes" if random.random() < 0.90 else "No"

    if bmi < 25:
        weekly_exercise_hours = random.randint(3,12)
        sleep_hours = round(random.uniform(7,9),1)
        diet_type = random.choices(['Mediterranean','Omnivore','Vegetarian','Pescatarian','Vegan','Keto'], weights=[35,30,12,10,5,8],k=1)[0]
    elif bmi < 30:
        weekly_exercise_hours = random.randint(1,8)
        sleep_hours = round(random.uniform(6.5,8.5),1)
        diet_type = random.choices(['Omnivore','Mediterranean','Keto','Vegetarian'],weights=[45,30,15,10],k=1)[0]
    else:
        weekly_exercise_hours = random.randint(0,5)
        sleep_hours = round(random.uniform(5.5,8),1)
        diet_type = random.choices(['Omnivore','Mediterranean','Keto'],weights=[60,25,15],k=1)[0]    

    if age <= 40:
        last_medical_check = (datetime.now() - timedelta(days=random.randint(180, 365*2))).strftime('%Y-%m-%d')
    else:
        last_medical_check = (datetime.now() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')

    conditions = []

    if bmi >= 30 and random.random() < 0.35:
        conditions.append("Hypertension")

    if bmi >= 30 and random.random() < 0.20:
        conditions.append("Diabetes")

    if is_smoker == "Yes" and random.random() < 0.15:
        conditions.append("Asthma")

    if age >= 55 and random.random() < 0.20:
        conditions.append("Arthritis")

    if not conditions:
        conditions.append("None")

    allergies = []

    if random.random() < 0.18:
        allergies.append("Pollen")

    if random.random() < 0.12:
        allergies.append("Dust")

    if random.random() < 0.08:
        allergies.append("Food")

    if random.random() < 0.05:
        allergies.append("Medication")

    if not allergies:
        allergies.append("None")

    return {
        'blood_type': random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']),
        'has_insurance': has_insurance,
        'is_smoker': is_smoker,
        'last_medical_check': last_medical_check,
        'bmi': round(bmi, 1),
        'bmi_category': 'Underweight' if bmi < 18.5 else 'Normal' if bmi < 25 else 'Overweight' if bmi < 30 else 'Obese',
        'weekly_exercise_hours': weekly_exercise_hours,
        'alcohol_consumption': random.choice(['None', 'Low', 'Moderate', 'High']),
        'diet_type': diet_type,
        'sleep_hours': sleep_hours,
        'chronic_conditions': ', '.join(conditions),
        'allergies': ', '.join(allergies)
    }

#Generate mortgage probability
def random_mortgage(age, salary):

    probability = 0.10
    if age >= 30:
        probability += 0.25
    if age >= 40:
        probability += 0.15
    if salary >= 2500:
        probability += 0.10
    if salary >= 4000:
        probability += 0.10
    probability = min(probability,0.80)

    return "Yes" if random.random() < probability else "No"

#Generate financial data
def random_financial_data(salary, experience, age):
    credit_score = min(850,max(300,int(random.gauss(620 + experience * 4,60))))
    has_mortgage = random_mortgage(age,salary)
    housing_cost = salary * random.uniform(0.20,0.35)

    if has_mortgage == "Yes":
        housing_cost *= random.uniform(1.15,1.35)

    food_expenses = salary * random.uniform(0.10,0.18)
    transportation_cost = salary * random.uniform(0.05,0.12)
    total_expenses = housing_cost + food_expenses + transportation_cost
    monthly_disposable_income = max(0,salary - total_expenses)
    savings = monthly_disposable_income * random.uniform(4,12)
    investment_portfolio_value = savings * random.uniform(0.5,3) if savings > 0 else 0
    debt_factor = (850 - credit_score) / 850
    debt_amount = salary * random.uniform(0,8) * debt_factor

    return {
        'credit_score': round(credit_score),
        'housing_cost': round(housing_cost,2),
        'food_expenses': round(food_expenses,2),
        'transportation_cost': round(transportation_cost,2),
        'debt_amount': round(debt_amount,2),
        'savings': round(savings,2),
        'investment_portfolio_value': round(investment_portfolio_value,2),
        'monthly_disposable_income': round(monthly_disposable_income,2),
        'has_mortgage': has_mortgage
    }

#Generate purchase history
def random_purchase_history(user_id, num_purchases=random.randint(1, 10)):
    purchases = []
    categories = ['Electronics', 'Clothing', 'Food', 'Entertainment', 'Travel', 'Health', 'Other']
    
    for _ in range(num_purchases):
        purchase_date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        purchases.append({
            'user_id': user_id,
            'purchase_date': purchase_date,
            'amount': round(random.uniform(10, 2000), 2),
            'category': random.choice(categories),
            'payment_method': random.choice(['Credit Card', 'Debit Card', 'Cash', 'Digital Wallet']),
            'store': random.choice(['Amazon', 'Walmart', 'Local Store', 'Specialty Shop', 'Online Marketplace'])
        })
    
    return purchases

#Generate phone number
def random_phone(nationality=None):
    phone_formats = {
         # AMERICA
    'Argentina': f"+54 9 11 {random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
    'Brazil': f"+55 {random.randint(11, 99)} 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
    'Canada': f"+1 {random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
    'Chile': f"+56 9 {random.randint(1000, 9999)} {random.randint(1000, 9999)}",
    'Colombia': f"+57 {random.randint(300, 399)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
    'Mexico': f"+52 {random.randint(1, 9)}{random.randint(10, 99)} {random.randint(1000, 9999)} {random.randint(1000, 9999)}",
    'Peru': f"+51 9{random.randint(10, 99)} {random.randint(100, 999)} {random.randint(100, 999)}",
    'United States': f"+1 {random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
    'Uruguay': f"+598 9{random.randint(100, 999)} {random.randint(1000, 9999)}",
    'Costa Rica': f"+506 {random.randint(6000, 7999)} {random.randint(1000, 9999)}",
    'Dominican Republic': f"+1 809 {random.randint(200, 999)} {random.randint(1000, 9999)}",
    
    # EUROPE
    'France': f"+33 {random.randint(1, 9)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}",
    'Germany': f"+49 {random.randint(150, 199)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
    'Italy': f"+39 3{random.randint(10, 99)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
    'Netherlands': f"+31 6 {random.randint(100, 999)} {random.randint(1000, 9999)}",
    'Poland': f"+48 {random.randint(500, 799)} {random.randint(100, 999)} {random.randint(100, 999)}",
    'Portugal': f"+351 9{random.randint(10, 99)} {random.randint(100, 999)} {random.randint(100, 999)}",
    'Russia': f"+7 {random.randint(900, 999)} {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}",
    'Spain': f"+34 {random.randint(600, 699)} {random.randint(100, 999)} {random.randint(100, 999)}",
    'Sweden': f"+46 {random.randint(70, 79)} {random.randint(100, 999)} {random.randint(100, 999)}",
    'United Kingdom': f"+44 {random.randint(7000, 7999)} {random.randint(100, 999)} {random.randint(100, 999)}",
    'Ukraine': f"+380 {random.randint(50, 99)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
    
    # ASIA
    'India': f"+91 {random.randint(70000, 99999)} {random.randint(10000, 99999)}",
    'Japan': f"+81 {random.randint(70, 89)} {random.randint(1000, 9999)} {random.randint(1000, 9999)}",
    'Philippines': f"+63 {random.randint(900, 999)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
    'South Korea': f"+82 {random.randint(10, 19)} {random.randint(1000, 9999)} {random.randint(1000, 9999)}",
    'Thailand': f"+66 {random.randint(80, 89)} {random.randint(100, 999)} {random.randint(100, 999)}",
    'Turkey': f"+90 {random.randint(500, 599)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
    'Malaysia': f"+60 1{random.randint(200, 999)} {random.randint(100, 999)} {random.randint(100, 999)}",
    'Sri Lanka': f"+94 7{random.randint(0, 9)} {random.randint(100, 999)} {random.randint(100, 999)}",
    'Singapore': f"+65 9{random.randint(0, 9)}{random.randint(100, 999)} {random.randint(1000, 9999)}",
    
    # AFRICA
    'Algeria': f"+213 {random.randint(500, 799)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}",
    'South Africa': f"+27 {random.randint(60, 79)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
    'Malawi': f"+265 {random.randint(888, 999)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}",
    'Malta': f"+356 {random.randint(7000, 7999)} {random.randint(1000, 9999)}",
    
    # OCEANIA
    'Australia': f"+61 4{random.randint(00, 99)} {random.randint(100, 999)} {random.randint(100, 999)}",
    'New Zealand': f"+64 {random.randint(20, 29)} {random.randint(100, 999)} {random.randint(100, 999)}",
    }
    
    if nationality and nationality in phone_formats:
        return phone_formats[nationality]
    
    # Generic format for other countries
    return f"+{random.randint(1, 99)} {random.randint(100, 999)}-{random.randint(100, 9999)}"

#Generate geographic location data
def random_address(nationality):
    # Suppress specific pgeocode warnings for problematic postal systems
    warning_messages = [
        "contains 4-digit postal codes which were replaced with a new system",
        "contains postal codes that are not numeric",
        "postal code format may not be accurate",
        "postal codes do not follow standard format",
        "The Argentina data file contains 4-digit postal codes*"
    ]
    
    for warning_msg in warning_messages:
        warnings.filterwarnings("ignore", message=warning_msg)
    
    # Get the ISO code for pgeocode
    iso_code = COUNTRY_TO_ISO[nationality]
    
    # Initialize pgeocode for the country
    nomi = pgeocode.Nominatim(iso_code)
    
    # Retrieve ALL locations for the country 
    try:
        lugares = nomi.query_location("")
    except:
        # If the empty query fails, retry with a high limit
        lugares = nomi.query_location("", top_k=10000)
    
    if lugares.empty:
        raise ValueError(f"No se encontraron datos de ubicación para {nationality} ({iso_code})")
    
    # Keep only rows with all required data
    datos_completos = lugares[
        lugares['latitude'].notna() & 
        lugares['longitude'].notna() & 
        lugares['postal_code'].notna() &
        lugares['place_name'].notna()
    ].copy()
    
    if datos_completos.empty:
        raise ValueError(f"No se encontraron ciudades con datos completos para {nationality} ({iso_code})")
    
    # Select a random city from those with complete data
    ciudad_info = datos_completos.sample(n=1).iloc[0]
    
    # Extract state/province - If empty, use the city name
    estado = ''
    if 'state_name' in ciudad_info and pd.notna(ciudad_info['state_name']):
        estado = ciudad_info['state_name']
    elif 'county_name' in ciudad_info and pd.notna(ciudad_info['county_name']):
        estado = ciudad_info['county_name']
    elif 'community_name' in ciudad_info and pd.notna(ciudad_info['community_name']):
        estado = ciudad_info['community_name']
    
    # If the state is still empty, use the city name
    if not estado:
        estado = ciudad_info['place_name']
    
    # Apply country-specific postal code corrections
    zip_code = str(ciudad_info['postal_code'])
    
    # Apply country-specific formats when necessary
    if nationality == 'Argentina':
        # Current Argentine format: Letter + 4 digits + 3 letters (e.g. C1000ABC)
        if zip_code.isdigit() and len(zip_code) == 4:
            first_letter = random.choice(['C', 'B', 'A', 'D', 'E', 'F', 'G', 'H', 'J', 'K'])
            last_letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
            zip_code = f"{first_letter}{zip_code}{last_letters}"
    
    elif nationality == 'Canada':
        # Canadian format: A1A 1A1 (alternating letter-number-letter)
        if len(zip_code) != 7 and zip_code.replace(' ', '').isalnum():
            letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            numbers = '0123456789'
            zip_code = f"{random.choice(letters)}{random.choice(numbers)}{random.choice(letters)} {random.choice(numbers)}{random.choice(letters)}{random.choice(numbers)}"
    
    elif nationality == 'United Kingdom':
        # UK format: AA1 1AA
        if len(zip_code) != 8 and ' ' not in zip_code:
            letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            numbers = '0123456789'
            zip_code = f"{random.choice(letters)}{random.choice(letters)}{random.choice(numbers)} {random.choice(numbers)}{random.choice(letters)}{random.choice(letters)}"
    
    elif nationality == 'Netherlands':
        # Dutch format: 1234 AB (4 digits + space + 2 letters)
        if not (len(zip_code) == 7 and zip_code[4] == ' ' and 
                zip_code[:4].isdigit() and zip_code[5:].isalpha()):
            numbers = f"{random.randint(1000, 9999)}"
            letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))
            zip_code = f"{numbers} {letters}"
    
    # Return the data
    return {
        'country': nationality,
        'city': ciudad_info['place_name'],
        'state': estado,
        'zip_code': zip_code,
        'latitude': float(ciudad_info['latitude']),
        'longitude': float(ciudad_info['longitude']),
    }

# ===== COMPLETE RANDOM DATA =====
# Generate data for all related tables

def generate_relational_person():
    # Basic user data
    sex = random_sex()
    nationality = random_nationality()
    birth_date = random_date()
    name = get_culturally_appropriate_name(sex, nationality)
    surname = get_culturally_appropriate_surname(nationality)
    # Calculate exact age
    birth_date_dt = datetime.strptime(birth_date, '%Y-%m-%d')
    today = datetime.now()
    age = today.year - birth_date_dt.year - ((today.month, today.day) < (birth_date_dt.month, birth_date_dt.day)) 

    marital_status = random_marital_status()
    height = random.randint(150, 200)
    weight = random.randint(50, 120)
    education_level = random_education()
    
    # Generate all structured data
    user_data = {
        'name': name,
        'surname': surname,
        'email': f"{name.lower()}.{surname.lower()}{random.randint(1, 99)}@{random.choice(['gmail.com', 'outlook.com', 'yahoo.com'])}",
        'birth_date': birth_date,
        'nationality': nationality,
        'marital_status': marital_status,
        'sex': sex,
        'height': height,
        'weight': weight,
        'phone': random_phone(nationality)
    }

    address_data = random_address(nationality)
      
    # Salary is required first for some related data
    employment_data = random_employment_data(age, education_level)
    salary = employment_data['salary']
    family_data = random_family_data(age, marital_status, salary)
    education_data = random_education_data(education_level,today.year,employment_data['job_title'],age)
    health_data = random_health_data(age, weight, height)
    financial_data = random_financial_data(salary,employment_data['years_experience'],age)
    
    return {
        'users': user_data,
        'addresses': address_data,
        'family': family_data,
        'education': education_data,
        'employment': employment_data,
        'health': health_data,
        'financial': financial_data,
        'purchases': None  # Will be generated after the user ID is available
    }