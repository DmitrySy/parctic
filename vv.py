import requests
import pandas as pd
import sqlite3

def get_vacancies(skills, pages=10):
    res = []
    for indx, skill in enumerate(skills):
        print(f'\ncollecting <{skill}> ({indx+1} of {len(skills)})')
        for page in range(pages):
            params = {
                'text': f'{skill}',
                'page': page,
                'per_page': 100,
                'only_with_salary': 'true',
            }
            req = requests.get('https://api.hh.ru/vacancies/', params).json()
            if 'items' in req.keys():
                res.extend(req['items'])
            print('|', end='')
    return res

def is_programming_related(title):
    programming_keywords = [
        'программист', 'разработчик', 'developer', 'software', 'engineer', 'programmer'
    ]
    title_lower = title.lower()
    return any(keyword in title_lower for keyword in programming_keywords)

# Your skills
skills = ['skill_1', 'skill_2']

# Collecting vacancy data
vacancies_data = get_vacancies(skills)

# Creating DataFrame
df = pd.DataFrame(vacancies_data)

# Filtering data
df_filtered = df[df['name'].apply(is_programming_related)]

# Saving original data to CSV
df.to_csv('vacancies.csv', index=False)

# Saving filtered data to a new CSV file
df_filtered.to_csv('filtered_vacancies.csv', index=False)

# Saving data to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Creating tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS vacancies (
    id TEXT PRIMARY KEY,
    name TEXT,
    area_name TEXT,
    salary_from REAL,
    salary_to REAL,
    employer_name TEXT,
    published_at TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS filtered_vacancies (
    id TEXT PRIMARY KEY,
    name TEXT,
    area_name TEXT,
    salary_from REAL,
    salary_to REAL,
    employer_name TEXT,
    published_at TEXT
)
''')

# Inserting data into vacancies table
for index, row in df.iterrows():
    cursor.execute('''
    INSERT OR IGNORE INTO vacancies (id, name, area_name, salary_from, salary_to, employer_name, published_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        row['id'], 
        row['name'], 
        row['area']['name'], 
        row['salary']['from'], 
        row['salary']['to'], 
        row['employer']['name'], 
        row['published_at']
    ))

# Inserting data into filtered_vacancies table
for index, row in df_filtered.iterrows():
    cursor.execute('''
    INSERT OR IGNORE INTO filtered_vacancies (id, name, area_name, salary_from, salary_to, employer_name, published_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        row['id'], 
        row['name'], 
        row['area']['name'], 
        row['salary']['from'], 
        row['salary']['to'], 
        row['employer']['name'], 
        row['published_at']
    ))

conn.commit()
conn.close()

print("Data collected and filtered. Original data saved in 'vacancies.csv'. Filtered data saved in 'filtered_vacancies.csv'. Data also saved in 'database.db'.")