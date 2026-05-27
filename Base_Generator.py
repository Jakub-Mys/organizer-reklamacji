import sqlite3
import os
from complaints_API import init_db

DB_FILE = os.getenv("DB_FILE", "baza_reklamacji.db")

def seed_database():
    init_db()
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM reklamacje")
        if cursor.fetchone()[0] == 0:
            reklamacje_testowe = [
                ("Jan Kowalski", "Telewizor nie włącza się po wyjęciu z pudełka", "Przyjęte", "2026-05-27", "2026-05-27"),
                ("Anna Nowak", "Pęknięta matryca w laptopie", "W toku", "2026-05-17", "2026-05-17")
            ]
            cursor.executemany(
                """
                INSERT INTO reklamacje (klient, opis, status, data_zgloszenia, data_startu_odliczania)
                VALUES (?, ?, ?, ?, ?)
                """,
                reklamacje_testowe
            )

if __name__ == "__main__":
    seed_database()