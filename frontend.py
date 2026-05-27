import os
import streamlit as st
import requests

# Pobieranie adresu API ze zmiennych środowiskowych
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/reklamacje")

st.set_page_config(page_title="Obsługa Reklamacji", layout="wide")
st.title("System Obsługi Reklamacji")

with st.expander("➕ Dodaj nową reklamację", expanded=False):
    with st.form("nowa_reklamacja_form"):
        klient = st.text_input("Imię i nazwisko klienta")
        opis = st.text_area("Opis problemu")
        submit_button = st.form_submit_button("Zapisz w systemie")

        if submit_button:
            if klient and opis:
                try:
                    response = requests.post(API_URL, json={"klient": klient, "opis": opis})
                    response.raise_for_status()
                    st.success("Reklamacja została dodana pomyślnie!")
                    st.rerun()
                except requests.exceptions.RequestException:
                    st.error("Błąd podczas zapisywania. Sprawdź połączenie z serwerem API.")
            else:
                st.error("Wypełnij wszystkie pola!")

st.divider()

try:
    response = requests.get(API_URL)
    response.raise_for_status()
    reklamacje = response.json()
except requests.exceptions.RequestException:
    st.error("Błąd połączenia z bazą danych. Upewnij się, że API jest włączone.")
    reklamacje = []

reklamacje_otwarte = [r for r in reklamacje if r['status'] != 'Zakończone']
reklamacje_zakonczone = [r for r in reklamacje if r['status'] == 'Zakończone']

kolory_hex = {
    "CZERWONY": "#ff4b4b",
    "POMARAŃCZOWY": "#ffa500",
    "ZIELONY": "#00cc66"
}

zakladka_otwarte, zakladka_zakonczone = st.tabs(["📂 Reklamacje Otwarte", "✅ Reklamacje Zakończone"])

with zakladka_otwarte:
    if not reklamacje_otwarte:
        st.info("Brak otwartych reklamacji.")

    for rek in reklamacje_otwarte:
        kolor = kolory_hex.get(rek["alert_kolor"], "#ffffff")

        with st.container(border=True):
            kolumna_dane, kolumna_akcje = st.columns([3, 2])

            with kolumna_dane:
                st.markdown(f"### Numer reklamacji: #{rek['id']}")
                st.markdown(f"**Klient:** {rek['klient']}")
                st.caption(f"Opis: {rek['opis']}")
                st.caption(f"Data przyjęcia: {rek['data_zgloszenia']}")

            with kolumna_akcje:
                st.markdown(f"<h4 style='color: {kolor};'>Pozostało dni: {rek['dni_do_konca_terminu']}</h4>",
                            unsafe_allow_html=True)

                aktualny_status = rek['status']
                lista_statusow = ["Przyjęte", "W toku", "Wysłane do producenta", "Oczekuje na odbiór klienta",
                                  "Zakończone"]

                nowy_status = st.selectbox(
                    "Zmień status:",
                    options=lista_statusow,
                    index=lista_statusow.index(aktualny_status),
                    key=f"status_{rek['id']}"
                )

                if st.button("💾 Zapisz zmianę", key=f"zapisz_{rek['id']}"):
                    if nowy_status != aktualny_status:
                        try:
                            update_response = requests.put(f"{API_URL}/{rek['id']}/status", json={"status": nowy_status})
                            update_response.raise_for_status()
                            st.rerun()
                        except requests.exceptions.RequestException:
                            st.error("Wystąpił błąd podczas aktualizacji statusu.")

with zakladka_zakonczone:
    if not reklamacje_zakonczone:
        st.info("Brak zakończonych reklamacji.")

    for rek in reklamacje_zakonczone:
        with st.container(border=True):
            st.markdown(f"### Numer reklamacji: #{rek['id']} (Zakończona)")
            st.markdown(f"**Klient:** {rek['klient']}")
            st.caption(f"Opis: {rek['opis']}")