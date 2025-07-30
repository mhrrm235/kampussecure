import sqlite3
import datetime
import os
import csv

DB_PATH = 'database/kampussecure.db'
HISTORY_CSV = 'reports/history.csv'

def log_scan_result(target, result, scan_type='Nmap & WhatWeb'):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Simpan ke SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT,
            scan_type TEXT,
            result TEXT,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO scan_logs (target, scan_type, result, timestamp) VALUES (?, ?, ?, ?)
    ''', (target, scan_type, result, timestamp))
    conn.commit()
    conn.close()

    # Simpan juga ke history.csv
    os.makedirs(os.path.dirname(HISTORY_CSV), exist_ok=True)
    with open(HISTORY_CSV, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, target, scan_type, result[:100] + "..."])  # Log ringkas
