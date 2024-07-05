from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import subprocess
import threading

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('vacancies.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS vacancies (
                            id INTEGER PRIMARY KEY,
                            Title TEXT,
                            Link TEXT,
                            City TEXT,
                            Position TEXT,
                            Level TEXT,
                            Salary TEXT)'''
                       )

    query = 'SELECT * FROM vacancies WHERE 1=1'
    params = []

    city = request.args.get('city')
    if city:
        cities = [c.strip() for c in city.split(',')]
        city_clauses = ' OR '.join('City LIKE ?' for _ in cities)
        query += f' AND ({city_clauses})'
        params.extend(f'%{c}%' for c in cities)

    position = request.args.get('position')
    if position:
        positions = [p.strip() for p in position.split(',')]
        position_clauses = ' OR '.join('Position LIKE ?' for _ in positions)
        query += f' AND ({position_clauses})'
        params.extend(f'%{p}%' for p in positions)

    level = request.args.get('level')
    if level:
        levels = [l.strip() for l in level.split(',')]
        level_clauses = ' OR '.join('Level LIKE ?' for _ in levels)
        query += f' AND ({level_clauses})'
        params.extend(f'%{l}%' for l in levels)

    vacancies = conn.execute(query, params).fetchall()
    total_vacancies = len(vacancies) 
    conn.close()
    return render_template('index.html', vacancies=vacancies, total_vacancies=total_vacancies)

@app.route('/start-parsing', methods=['POST'])
def start_parsing():
    data = request.json
    city = data.get('city', '')
    position = data.get('position', '')
    skills = data.get('skills', '')

    try:
        threading.Thread(target=run_parser, args=(city, position, skills)).start()
        return jsonify({'message': 'Парсинг запущен.', 'status': 'success'})
    except Exception as e:
        return jsonify({'message': f'Произошла ошибка: {str(e)}', 'status': 'error'})

def run_parser(city, position, skills):
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'update_database_script.py')
    subprocess.run(['python', script_path, '--cities', city, '--posts', position, '--levels', skills], check=True)

if __name__ == '__main__':
    app.run(debug=True)