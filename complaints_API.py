import os
import sqlite3
from datetime import date, timedelta
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Strona Obsługi Reklamacji")
DB_FILE = os.getenv("DB_FILE", "baza_reklamacji.db")


def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS reklamacje (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                klient TEXT NOT NULL,
                opis TEXT NOT NULL,
                status TEXT NOT NULL,
                data_zgloszenia TEXT NOT NULL,
                data_startu_odliczania TEXT NOT NULL
            )
            """
        )


init_db()


def analizuj_termin(data_startu_str: str) -> tuple[int, str]:
    data_startu = date.fromisoformat(data_startu_str)
    dni_od_startu = (date.today() - data_startu).days
    dni_do_konca = 14 - dni_od_startu

    if dni_do_konca < 0:
        return dni_do_konca, "CZERWONY"
    elif dni_do_konca <= 5:
        return dni_do_konca, "POMARAŃCZOWY"
    return dni_do_konca, "ZIELONY"


class ReklamacjaCreate(BaseModel):
    klient: str
    opis: str

class ReklamacjaStatusUpdate(BaseModel):
    status: str

class ReklamacjaResponse(BaseModel):
    id: int
    klient: str
    opis: str
    status: str
    data_zgloszenia: date
    data_startu_odliczania: date
    dni_do_konca_terminu: int
    alert_kolor: str

@app.post("/reklamacje", response_model=ReklamacjaResponse, status_code=201)
def utworz_reklamacje(rek_in: ReklamacjaCreate):
    dzisiaj = date.today().isoformat()

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO reklamacje (klient, opis, status, data_zgloszenia, data_startu_odliczania)
            VALUES (?, ?, ?, ?, ?)
            """,
            (rek_in.klient, rek_in.opis, "Przyjęte", dzisiaj, dzisiaj),
        )
        nowe_id = cursor.lastrowid

    dni_do_konca, kolor = analizuj_termin(dzisiaj)
    return {
        "id": nowe_id,
        "klient": rek_in.klient,
        "opis": rek_in.opis,
        "status": "Przyjęte",
        "data_zgloszenia": date.today(),
        "data_startu_odliczania": date.today(),
        "dni_do_konca_terminu": dni_do_konca,
        "alert_kolor": kolor,
    }

@app.get("/reklamacje", response_model=List[ReklamacjaResponse])
def pobierz_reklamacje():
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, klient, opis, status, data_zgloszenia, data_startu_odliczania FROM reklamacje"
        )
        rows = cursor.fetchall()

    wynik = []
    for row in rows:
        dni_do_konca, kolor = analizuj_termin(row["data_startu_odliczania"])
        wynik.append(
            {
                "id": row["id"],
                "klient": row["klient"],
                "opis": row["opis"],
                "status": row["status"],
                "data_zgloszenia": date.fromisoformat(row["data_zgloszenia"]),
                "data_startu_odliczania": date.fromisoformat(row["data_startu_odliczania"]),
                "dni_do_konca_terminu": dni_do_konca,
                "alert_kolor": kolor,
            }
        )
    return wynik

@app.put("/reklamacje/{id}/status", response_model=ReklamacjaResponse)
def aktualizuj_status(id: int, update_data: ReklamacjaStatusUpdate):
    dozwolone_statusy = [
        "Przyjęte",
        "W toku",
        "Wysłane do producenta",
        "Oczekuje na odbiór klienta",
        "Zakończone",
    ]
    if update_data.status not in dozwolone_statusy:
        raise HTTPException(status_code=400, detail="Nieprawidłowy status.")

    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM reklamacje WHERE id = ?", (id,))
        rek = cursor.fetchone()

        if not rek:
            raise HTTPException(status_code=404, detail="Reklamacja nie znaleziona")

        nowy_status = update_data.status
        nowa_data_startu = rek["data_startu_odliczania"]

        if nowy_status == "Wysłane do producenta":
            nowa_data_startu = date.today().isoformat()

        cursor.execute(
            """
            UPDATE reklamacje 
            SET status = ?, data_startu_odliczania = ? 
            WHERE id = ?
            """,
            (nowy_status, nowa_data_startu, id),
        )

    dni_do_konca, kolor = analizuj_termin(nowa_data_startu)
    return {
        "id": rek["id"],
        "klient": rek["klient"],
        "opis": rek["opis"],
        "status": nowy_status,
        "data_zgloszenia": date.fromisoformat(rek["data_zgloszenia"]),
        "data_startu_odliczania": date.fromisoformat(nowa_data_startu),
        "dni_do_konca_terminu": dni_do_konca,
        "alert_kolor": kolor,
    }