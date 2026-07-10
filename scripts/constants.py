# ======================================================
# COUNTRY CONFIGURATION
# ======================================================

# Configuration of Mimesis by lenguages/regions
COUNTRY_TO_MIMESIS_LOCALE = {
   # AMÉRICA
    'Argentina': 'es',
    'Brazil': 'pt-br',
    'Canada': 'en',
    'Chile': 'es-MX',
    'Colombia': 'es-MX',
    'Mexico': 'es-MX',
    'United States': 'es-MX',
    'Peru': 'es-MX',
    'Uruguay': 'es-MX',
    'Costa Rica': 'es-MX',
    'Dominican Republic': 'es-MX',

    # EUROPE
    'France': 'fr',
    'Germany': 'en',
    'Italy': 'it',
    'Netherlands': 'en',
    'Poland': 'en',
    'Portugal': 'pt',
    'Russia': 'en',  
    'Spain': 'es',
    'Sweden': 'en',
    'United Kingdom': 'en',
    'Ukraine': 'en',  

    # ASIA
    'India': 'en',
    'Japan': 'en',
    'Philippines': 'en',
    'South Korea': 'en',
    'Thailand': 'en',
    'Turkey': 'en',
    'Malaysia': 'en',
    'Sri Lanka': 'en',
    'Singapore': 'en',

    # ÁFRICA
    'Algeria': 'es',
    'South Africa': 'es',
    'Malawi': 'es',
    'Malta': 'es',

    # OCEANÍA
    'Australia': 'en',
    'New Zealand': 'en'
}

# Dictionary Name of the country -> Code ISO for pgeocode
COUNTRY_TO_ISO = {
    'Argentina': 'AR',
    'Brazil': 'BR',
    'Canada': 'CA',
    'Chile': 'CL',
    'Colombia': 'CO',
    'Mexico': 'MX',
    'United States': 'US',
    'Peru': 'PE',
    'Uruguay': 'UY',
    'Costa Rica': 'CR',
    'Dominican Republic': 'DO',
    'France': 'FR',
    'Germany': 'DE',
    'Italy': 'IT',
    'Netherlands': 'NL',
    'Poland': 'PL',
    'Portugal': 'PT',
    'Russia': 'RU',
    'Spain': 'ES',
    'Sweden': 'SE',
    'United Kingdom': 'GB',
    'Ukraine': 'UA',
    'India': 'IN',
    'Japan': 'JP',
    'Philippines': 'PH',
    'South Korea': 'KR',
    'Thailand': 'TH',
    'Turkey': 'TR',
    'Malaysia': 'MY',
    'Sri Lanka': 'LK',
    'Singapore': 'SG',
    'Algeria': 'DZ',
    'South Africa': 'ZA',
    'Malawi': 'MW',
    'Malta': 'MT',
    'Australia': 'AU',
    'New Zealand': 'NZ'
}

# ======================================================
# EMPLOYMENT CONFIGURATION
# ======================================================

#Dictionary with jobs, company and size
# Jobs possibilities by education level
JOB_BY_EDUCATION = {
    'No degree': [
        'Farmer',
        'Chef'
    ],
    'High School': [
        'Farmer',
        'Chef',
        'Artist'
    ],
    'Technical': [
        'Developer',
        'Designer',
        'Engineer'
    ],
    'Bachelor': [
        'Developer',
        'Engineer',
        'Teacher',
        'Designer'
    ],
    'Master': [
        'Developer',
        'Engineer',
        'Scientist',
        'Architect'
    ],
    'PhD': [
        'Scientist',
        'Doctor'
    ]
}

# Company by Job
JOB_COMPANIES = {
    'Engineer': {
        'Técnicas Reunidas': 'Small (1-50)',
        'IDOM': 'Small (1-50)',
        'Hilti': 'Medium (51-500)',
        'Worley': 'Medium (51-500)',
        'Arup': 'Large (501-5000)',
        'Fluor Corporation': 'Large (501-5000)',
        'Stantec': 'Large (501-5000)',
        'Siemens': 'Enterprise (5000+)',
        'Schneider Electric': 'Enterprise (5000+)',
        'Bechtel': 'Enterprise (5000+)'
    },
    'Teacher': {
        'Superprof': 'Small (1-50)',
        'Open English': 'Small (1-50)',
        'Rosetta Stone': 'Medium (51-500)',
        'Cambly': 'Medium (51-500)',
        'Berlitz': 'Large (501-5000)',
        'Kumon': 'Large (501-5000)',
        'EF Education First': 'Large (501-5000)',
        'Pearson': 'Enterprise (5000+)',
        'McGraw Hill': 'Enterprise (5000+)',
        'Cengage Learning': 'Enterprise (5000+)'
    },
    'Doctor': {
        'Clínica Universidad de Navarra': 'Small (1-50)',
        'Hospital Sant Joan de Déu': 'Small (1-50)',
        'Cleveland Clinic Florida': 'Medium (51-500)',
        'Mayo Clinic Arizona': 'Medium (51-500)',
        'Massachusetts General Hospital': 'Large (501-5000)',
        'Johns Hopkins Hospital': 'Large (501-5000)',
        'Cedars-Sinai Medical Center': 'Large (501-5000)',
        'UnitedHealth Group': 'Enterprise (5000+)',
        'Johnson & Johnson': 'Enterprise (5000+)',
        'Mayo Clinic': 'Enterprise (5000+)'
    },
    'Artist': {
        'Laika Studios': 'Small (1-50)',
        'Cartoon Saloon': 'Small (1-50)',
        'Illumination Entertainment': 'Medium (51-500)',
        'Aardman Animations': 'Medium (51-500)',
        'Pixar Animation Studios': 'Large (501-5000)',
        'DreamWorks Animation': 'Large (501-5000)',
        'Netflix Animation': 'Large (501-5000)',
        'Walt Disney Studios': 'Enterprise (5000+)',
        'Warner Bros. Discovery': 'Enterprise (5000+)',
        'Universal Pictures': 'Enterprise (5000+)'
    },
    'Developer': {
        'Basecamp': 'Small (1-50)',
        'GitHub': 'Small (1-50)',
        'Atlassian': 'Medium (51-500)',
        'Slack Technologies': 'Medium (51-500)',
        'Adobe': 'Large (501-5000)',
        'Salesforce': 'Large (501-5000)',
        'ServiceNow': 'Large (501-5000)',
        'Microsoft': 'Enterprise (5000+)',
        'Google': 'Enterprise (5000+)',
        'Amazon': 'Enterprise (5000+)'
    },
    'Chef': {
        'El Celler de Can Roca': 'Small (1-50)',
        'Mugaritz': 'Small (1-50)',
        'The French Laundry': 'Medium (51-500)',
        'Alinea Group': 'Medium (51-500)',
        'Gordon Ramsay Restaurants': 'Large (501-5000)',
        'Nobu Hospitality': 'Large (501-5000)',
        'Momofuku Restaurant Group': 'Large (501-5000)',
        'McDonald\'s': 'Enterprise (5000+)',
        'Yum! Brands': 'Enterprise (5000+)',
        'Compass Group': 'Enterprise (5000+)'
    },
    'Architect': {
        'BIG - Bjarke Ingels Group': 'Small (1-50)',
        'Zaha Hadid Architects': 'Small (1-50)',
        'Snøhetta': 'Medium (51-500)',
        'Mecanoo': 'Medium (51-500)',
        'Foster + Partners': 'Large (501-5000)',
        'Perkins and Will': 'Large (501-5000)',
        'Kohn Pedersen Fox': 'Large (501-5000)',
        'Gensler': 'Enterprise (5000+)',
        'AECOM': 'Enterprise (5000+)',
        'Jacobs Solutions': 'Enterprise (5000+)'
    },
    'Farmer': {
        'Huerta de la Vega': 'Small (1-50)',
        'Finca Moncloa': 'Small (1-50)',
        'Rijk Zwaan': 'Medium (51-500)',
        'Seminis (Bayer)': 'Medium (51-500)',
        'John Deere Ibérica': 'Large (501-5000)',
        'Corteva Agriscience España': 'Large (501-5000)',
        'Grupo AN': 'Large (501-5000)',
        'Bayer Crop Science': 'Enterprise (5000+)',
        'Cargill': 'Enterprise (5000+)',
        'Syngenta Group': 'Enterprise (5000+)'
    },
    'Designer': {
        'Pentagram': 'Small (1-50)',
        'Smart Design': 'Small (1-50)',
        'IDEO': 'Medium (51-500)',
        'Frog Design': 'Medium (51-500)',
        'Philips Design': 'Large (501-5000)',
        'BMW Group Design': 'Large (501-5000)',
        'IKEA Design': 'Large (501-5000)',
        'Apple': 'Enterprise (5000+)',
        'Samsung Design': 'Enterprise (5000+)',
        'Tesla Design Studio': 'Enterprise (5000+)'
    },
    'Scientist': {
        'CRG - Centre for Genomic Regulation': 'Small (1-50)',
        'Institute for Bioengineering of Catalonia': 'Small (1-50)',
        'Novozymes': 'Medium (51-500)',
        'Illumina Spain': 'Medium (51-500)',
        'Amgen': 'Large (501-5000)',
        'Biogen': 'Large (501-5000)',
        'Thermo Fisher Scientific Iberia': 'Large (501-5000)',
        'Pfizer': 'Enterprise (5000+)',
        'Roche': 'Enterprise (5000+)',
        'Merck Group': 'Enterprise (5000+)'
    }
}

# Multiplier of salary by job
JOB_SALARY_MULTIPLIER = {

    'Developer':1.4,
    'Engineer':1.5,
    'Doctor':1.6,
    'Scientist':1.7,
    'Teacher':1.1,
    'Artist':0.9,
    'Chef':1.0,
    'Designer':1.2,
    'Architect':1.3,
    'Farmer':0.8
}