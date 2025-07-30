import sqlite3
import os

def init_db():
    conn = sqlite3.connect('database/kampussecure.db')
    cursor = conn.cursor()

    # Table: users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Table: scan_logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT,
            scan_type TEXT,
            result TEXT,
            timestamp TEXT
        )
    ''')

    # Table: edukasi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS edukasi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def insert_edukasi(title, content):
    conn = sqlite3.connect('database/kampussecure.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO edukasi (title, content)
        VALUES (?, ?)
    ''', (title, content))

    conn.commit()
    conn.close()
    print("Data inserted into edukasi table successfully.")

if __name__ == "__main__":
    init_db()
    # Tambah beberapa data edukasi sekaligus
    insert_edukasi("Apa Itu Phishing?", "Phishing adalah upaya untuk mendapatkan informasi sensitif seperti username, password, dan data kartu kredit dari korban dengan menyamar sebagai entitas tepercaya.")
    insert_edukasi("Tips Mengamankan Akun", "Gunakan password yang kuat, aktifkan autentikasi dua faktor (2FA), dan jangan klik link mencurigakan yang dikirim melalui email atau pesan.")
    insert_edukasi("Jenis-jenis Malware", "Virus, Worm, Trojan, Ransomware adalah beberapa jenis malware yang dapat merusak atau mencuri data dari perangkat Anda.")
    insert_edukasi("Pengenalan SQL", "SQL adalah bahasa yang digunakan untuk mengelola dan memanipulasi basis data.")
    insert_edukasi("Serangan Cyber", "Serangan cyber adalah upaya yang dilakukan oleh individu atau kelompok untuk menyerang sistem komputer, jaringan, atau perangkat digital dengan tujuan mencuri, merusak, atau mengganggu data dan layanan. Contoh serangan cyber meliputi DDoS, ransomware, dan hacking akun.")
    insert_edukasi("Bahaya Link Sembarangan", "Membagikan atau mengklik link sembarangan sangat berbahaya karena bisa saja link tersebut mengandung malware, phising, atau mengarahkan ke situs palsu yang mencuri data pribadi. Selalu pastikan link berasal dari sumber terpercaya sebelum membagikannya ke orang lain.")
    insert_edukasi("Bahayanya Serangan Cyber", "Serangan cyber dapat menyebabkan kerugian besar, seperti pencurian data pribadi, kerusakan sistem, kehilangan kepercayaan pengguna, bahkan kerugian finansial. Serangan yang berhasil dapat membuat data penting bocor ke publik, layanan lumpuh, atau perangkat terinfeksi malware. Oleh karena itu, penting untuk selalu waspada dan menerapkan langkah-langkah keamanan digital.")
