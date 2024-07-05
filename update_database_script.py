import requests
from bs4 import BeautifulSoup
import sqlite3
import argparse
import os

URL1 = "https://career.habr.com/vacancies"
URL2 = "https://career.habr.com"

def fetch_html(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    return response.text

def should_display_vacancy(vacancy_data, cities, posts, levels):
    city_check = all(city in (vacancy_data['City'] or '').lower() for city in cities)
    post_check = all(post in (vacancy_data['Position'] or '').lower() for post in posts)
    level_check = all(level in (vacancy_data['Level'] or '').lower() for level in levels)
    return city_check and post_check and level_check

def save_vacancy_to_db(vacancy_data):
    connection = sqlite3.connect("vacancies.db")
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO vacancies (Title, Link, City, Position, Level, Salary) 
                      VALUES (?, ?, ?, ?, ?, ?)''', 
                   (vacancy_data['Title'], 
                    vacancy_data['Link'], 
                    vacancy_data['City'], 
                    vacancy_data['Position'], 
                    vacancy_data['Level'], 
                    vacancy_data['Salary']))
    connection.commit()
    connection.close()

def parse_vacancy_card(card_html):
    soup = BeautifulSoup(card_html, 'html.parser')
    data = {
        'City': soup.select_one(".vacancy-card__meta").get_text(strip=True) if soup.select_one(".vacancy-card__meta") else None,
        'Level': soup.select_one(".vacancy-card__skills").get_text(strip=True) if soup.select_one(".vacancy-card__skills") else None,
        'Position': soup.select_one(".vacancy-card__title").get_text(strip=True) if soup.select_one(".vacancy-card__title") else None,
        'Salary': soup.select_one(".vacancy-card__salary").get_text(strip=True) if soup.select_one(".vacancy-card__salary") else "Не указана",
        'Title': soup.select_one(".vacancy-card__title").get_text(strip=True) if soup.select_one(".vacancy-card__title") else None,
        'Link': URL2 + soup.select_one(".vacancy-card__title a")['href'] if soup.select_one(".vacancy-card__title a") else None,
    }
    return data

def main():
    new_vacancies_count = 0
    if os.path.exists("vacancies.db"):
        os.remove("vacancies.db")
    
    parser = argparse.ArgumentParser(description="Парсинг вакансий")
    parser.add_argument('--cities', type=str, help='Города для парсинга, разделенные запятыми', default='')
    parser.add_argument('--posts', type=str, help='Должности для парсинга, разделенные запятыми', default='')
    parser.add_argument('--levels', type=str, help='Уровни для парсинга, разделенные запятыми', default='')
    
    args = parser.parse_args()
    cities = [c.strip().lower() for c in args.cities.split(',') if c.strip()]
    posts = [p.strip().lower() for p in args.posts.split(',') if p.strip()]
    levels = [l.strip().lower() for l in args.levels.split(',') if l.strip()]

    connection = sqlite3.connect("vacancies.db")
    with connection:
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS vacancies (
                            id INTEGER PRIMARY KEY,
                            Title TEXT,
                            Link TEXT,
                            City TEXT,
                            Position TEXT,
                            Level TEXT,
                            Salary TEXT)'''
                       )

    print("Доступные вакансии")

    page_number = 1
    
    while True:
        url = f"{URL1}?page={page_number}"
        html = fetch_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        vacancy_cards = soup.select(".vacancy-card")

        if not vacancy_cards:
            break
        
        for card_html in vacancy_cards:
            card_data = parse_vacancy_card(str(card_html))
            if should_display_vacancy(card_data, cities, posts, levels):
                print(f"Название: {card_data['Title']}")
                print(f"Ссылка: {card_data['Link']}")
                print(f"Город: {card_data['City']}")
                print(f"Должность: {card_data['Position']}")
                print(f"Уровень: {card_data['Level']}")
                print(f"Зарплата (Если она указана): {card_data['Salary']}")
                print("---------------------------------------")
                save_vacancy_to_db(card_data)
                new_vacancies_count += 1
        
        page_number += 1
    
    print(f"Новые вакансии: {new_vacancies_count}")
if __name__ == "__main__":
    main()