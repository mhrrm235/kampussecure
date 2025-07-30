import sqlite3

# Data edukasi yang ingin dimasukkan
edukasi_data = [
    ("Apa Itu Phishing?", "Phishing adalah upaya untuk mendapatkan informasi sensitif seperti username, password, dan data kartu kredit..."),
    ("Tips Mengamankan Akun", "Gunakan password yang kuat, aktifkan autentikasi dua faktor (2FA), dan jangan klik link mencurigakan..."),
    ("Jenis-jenis Malware", "Virus, Worm, Trojan, Ransomware... semuanya punya cara kerja berbeda dan dapat merugikan.")
]

def insert_edukasi():
    conn = sqlite3.connect('database/kampussecure.db')
    cursor = conn.cursor()
    cursor.executemany('INSERT INTO edukasi (title, content) VALUES (?, ?)', edukasi_data)
    conn.commit()
    conn.close()
    print("Data edukasi berhasil ditambahkan.")

if __name__ == "__main__":
    insert_edukasi()
