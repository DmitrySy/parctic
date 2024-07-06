from pywebio.input import *
from pywebio.output import *
import sqlite3

# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn, conn.cursor()

# Функция для отображения данных из базы данных
def show_data_from_db():
    conn, cursor = get_db_connection()
    cursor.execute('SELECT * FROM vacancies')
    data = cursor.fetchall()
    conn.close()
    
    put_table([['ID', 'Название', 'Зарплата']] + data)

# Функция для фильтрации данных по имени
def filter_data_by_name(name):
    conn, cursor = get_db_connection()
    cursor.execute('SELECT * FROM vacancies WHERE name LIKE ?', (f'%{name}%',))
    data = cursor.fetchall()
    conn.close()
    
    put_table([['ID', 'Название', 'Зарплата']] + data)

# Функция для фильтрации данных по диапазону зарплаты
def filter_data_by_salary(min_salary, max_salary):
    conn, cursor = get_db_connection()
    cursor.execute('SELECT * FROM vacancies WHERE salary BETWEEN ? AND ?', (min_salary, max_salary))
    data = cursor.fetchall()
    conn.close()
    
    put_table([['ID', 'Название', 'Зарплата']] + data)

# Создаем интерфейс для отображения данных
def show_data_interface():
    put_text("Данные из базы данных:")
    show_data_from_db()

# Создаем интерфейс для фильтрации данных по имени
def filter_data_by_name_interface():
    name = input("Введите название вакансии для фильтрации:", type=TEXT)
    put_text(f"Результаты фильтрации по названию '{name}':")
    filter_data_by_name(name)

# Создаем интерфейс для фильтрации данных по зарплате
def filter_data_by_salary_interface():
    min_salary = input("Введите минимальную зарплату (число):", type=NUMBER)
    max_salary = input("Введите максимальную зарплату (число):", type=NUMBER)
    put_text(f"Результаты фильтрации по зарплате от {min_salary} до {max_salary}:")
    filter_data_by_salary(min_salary, max_salary)

# Основная функция интерфейса
def main():
    while True:
        action = select("Выберите действие:", ['Показать данные', 'Фильтр по названию', 'Фильтр по зарплате'])
        
        if action == 'Показать данные':
            show_data_interface()
        elif action == 'Фильтр по названию':
            filter_data_by_name_interface()
        elif action == 'Фильтр по зарплате':
            filter_data_by_salary_interface()

# Запуск приложения
if __name__ == '__main__':
    import pywebio
    pywebio.start_server(main, port=8080)