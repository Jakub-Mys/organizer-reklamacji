**1. System Obsługi Reklamacji**

Ten program pomaga zarządzać procesem reklamacyjnym. Zapisuje zgłoszenia od klientów, pilnuje ustawowego, 14-dniowego terminu na rozpatrzenie sprawy i pozwala łatwo zmieniać statusy. Program sam ostrzega o zbliżającym się końcu terminu za pomocą kolorów (zielony, pomarańczowy, czerwony). Zmiana statusu na "Wysłane do producenta" automatycznie resetuje odliczanie.

**2. Szybki przegląd plików**

Cały system opiera się na kilku plikach, z których każdy odpowiada za inną część działania programu.

**2.1. Silnik i Serwer**

Plik complaints_API.py to serwer (API), który zarządza danymi. Zapisuje informacje w bazie danych i automatycznie wylicza, ile dni zostało na rozwiązanie sprawy.

**2.2. Wygląd aplikacji**

Plik frontend.py to przejrzysty panel wizualny. To w nim wyświetla się interfejs, w którym wpisujesz dane klienta, czytasz opisy problemów i klikasz, aby zmienić status reklamacji.

**2.3. Dane testowe Plik**

Base_Generator.py to pomocniczy skrypt. Gdy uruchomisz go raz na samym początku, stworzy bazę danych z dwoma przykładowymi zgłoszeniami:

```Python
reklamacje_testowe = [
    ("Jan Kowalski", "Telewizor nie włącza się po wyjęciu z pudełka", "Przyjęte", "2026-05-27", "2026-05-27"),
    ("Anna Nowak", "Pęknięta matryca w laptopie", "W toku", "2026-05-17", "2026-05-17")
]
```
**3. Jak uruchomić?**

Zanim uruchomisz program po raz pierwszy, musisz zainstalować wymagane pakiety. Wpisz w terminalu poniższe polecenie:

```Bash
pip install fastapi uvicorn streamlit requests
```
(Opcjonalnie) Jeśli chcesz załadować dane testowe, wpisz również 
```
python Base_Generator.py.
```

**-Windows:** Kliknij dwukrotnie plik Start.bat. **-Terminal Windows:** Wpisz w jednym oknie komendę: ```uvicorn api_do_reklamacji:app --reload``` a następnie w drugim, nowym oknie komendę: ```streamlit run frontend.py```

***Uwaga: Projekt znajduje się obecnie w fazie rozwoju i testów . Kolejne funkcje będą dodawane na bieżąco.***
