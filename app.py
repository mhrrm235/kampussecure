from flask import Flask, render_template, request, redirect, url_for, session
from Modul.scanner import run_scan
from Modul.edukasi import get_articles
from Modul.reporter import generate_pdf, generate_csv
from Modul.logger import log_scan_result
import os


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ganti dengan kunci rahasia yang aman

# Middleware: redirect ke login jika belum login (kecuali login & static)
from functools import wraps
from flask import request

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        import sqlite3
        db_path = os.path.join(os.path.dirname(__file__), 'Database', 'kampussecure.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Username atau password salah!')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/edukasi')
@login_required
def edukasi():
    articles = get_articles()
    return render_template('edukasi.html', articles=articles)



# Route GET untuk form scan
@app.route('/scan', methods=['GET', 'POST'])
@login_required
def scan():
    if request.method == 'POST':
        target = request.form['target']
        scan_result = run_scan(target)
        # Isi scan_type sesuai tools yang digunakan
        log_scan_result(target, scan_result, scan_type='Nmap & WhatWeb')
        return render_template('scan_results.html', result=scan_result)
    return render_template('scan.html')

# Route laporan hasil scan
import sqlite3
@app.route('/laporan')
@login_required
def laporan():
    db_path = os.path.join(os.path.dirname(__file__), 'Database', 'kampussecure.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT target, scan_type, result, timestamp FROM scan_logs ORDER BY timestamp DESC')
    logs = cursor.fetchall()
    conn.close()
    return render_template('laporan.html', logs=logs)



# Route logout
@app.route('/logout')
@login_required
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
