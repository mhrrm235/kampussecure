import sqlite3
from datetime import datetime

def log_scan(target, scan_type, result):
    conn = sqlite3.connect('database/kampussecure.db')
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
        INSERT INTO scan_logs (target, scan_type, result, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (target, scan_type, result, timestamp))

    conn.commit()
    conn.close()
