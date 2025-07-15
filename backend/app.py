from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import requests
import threading
import time

app = Flask(__name__)
CORS(app)

DB_PATH = 'weather.db'
import random
import datetime
CITIES = [
    'Cape Town', 'Johannesburg', 'Durban', 'Pretoria', 'Port Elizabeth',
    'Bloemfontein', 'Polokwane', 'Nelspruit', 'Kimberley', 'Mthatha'
]

# Initialize DB
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        temp REAL,
        condition TEXT,
        wind REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        alert TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

# Fetch weather and store in DB
def fetch_and_store_weather():
    weather_conditions = ['Clear', 'Clouds', 'Rain', 'Thunderstorm', 'Drizzle', 'Snow', 'Mist', 'Tornado']
    while True:
        for city in CITIES:
            temp = round(random.uniform(-5, 45), 1)
            condition = random.choice(weather_conditions)
            wind = round(random.uniform(0, 30), 1)
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('INSERT INTO weather (city, temp, condition, wind) VALUES (?, ?, ?, ?)',
                      (city, temp, condition, wind))
            # Extreme condition check
            alert = None
            if temp > 40 or temp < 0:
                alert = f'Extreme temperature: {temp}°C'
            elif wind > 20:
                alert = f'Extreme wind: {wind} m/s'
            elif condition in ['Thunderstorm', 'Tornado']:
                alert = f'Extreme weather: {condition}'
            if alert:
                c.execute('INSERT INTO alerts (city, alert) VALUES (?, ?)', (city, alert))
            conn.commit()
            conn.close()
        time.sleep(10)  # Update every 10 seconds for demo

@app.route('/weather')
def get_weather():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT city, temp, condition, wind, timestamp FROM weather WHERE timestamp >= datetime("now", "-15 minutes")')
    rows = c.fetchall()
    conn.close()
    return jsonify([{'city': r[0], 'temp': r[1], 'condition': r[2], 'wind': r[3], 'timestamp': r[4]} for r in rows])

@app.route('/alerts')
def get_alerts():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT city, alert, timestamp FROM alerts WHERE timestamp >= datetime("now", "-1 hour")')
    rows = c.fetchall()
    conn.close()
    return jsonify([{'city': r[0], 'alert': r[1], 'timestamp': r[2]} for r in rows])

if __name__ == '__main__':
    init_db()
    threading.Thread(target=fetch_and_store_weather, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
