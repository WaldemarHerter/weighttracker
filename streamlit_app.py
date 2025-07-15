<<<<<<< HEAD

# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils import init_db, update_entry, fetch_all, delete_entry, update_weight

# Seite konfigurieren
st.set_page_config(layout="wide", page_title="Weight Tracker")
st.header("📊 Weight Tracker App")

# MongoDB Connection
db_coll = init_db()

# Caching für Datenabruf
@st.cache_data(ttl=600)
def load_data():
    entries = fetch_all(db_coll)
    if not entries:
        return pd.DataFrame(columns=["date", "weight", "sports_activity"])
    df = pd.DataFrame(entries)
    df["_id"] = df["_id"].astype(str)
    df.set_index("_id", inplace=True)
    df.sort_values("date", inplace=True)
    df["date"] = pd.to_datetime(df["date"])
    return df

# Daten laden
df = load_data()

# Sidebar: Einträge verwalten
with st.sidebar:
    st.subheader("Neuen Eintrag hinzufügen")
    new_weight = st.number_input("Gewicht (kg)", min_value=0.0, format="%.1f", key="new_entry")
    entry_date = st.date_input("Datum", datetime.now(), key="entry_date")
    sports_activity = st.checkbox("Sports Activity")
    if st.button("Hinzufügen"):
        try:
            entry_id = update_entry(
                db_coll,
                entry_date.strftime("%Y-%m-%d"),
                new_weight,
                "Yes" if sports_activity else "No"
            )
            st.success(f"Eintrag {entry_id} hinzugefügt!")
            load_data.clear()
        except Exception as e:
            st.error(f"Fehler beim Hinzufügen: {e}")

    st.markdown("---")
    st.subheader("Eintrag löschen")
    delete_id = st.text_input("Eintrags-ID", key="delete_id")
    if st.button("Löschen"):
        if delete_id:
            deleted = delete_entry(db_coll, delete_id)
            if deleted:
                st.success(f"Eintrag {delete_id} gelöscht.")
                load_data.clear()
            else:
                st.warning("ID nicht gefunden.")
        else:
            st.warning("Bitte gib eine ID ein.")

    st.markdown("---")
    st.subheader("Eintrag bearbeiten")
    if not df.empty:
        edit_id = st.selectbox("Wähle ID zum Bearbeiten", options=df.index, key="edit_id")
        new_w = st.number_input(
            "Neues Gewicht (kg)",
            value=float(df.loc[edit_id, "weight"]),
            format="%.1f",
            key="edit_w"
        )
        if st.button("Aktualisieren", key="update_btn"):
            modified = update_weight(db_coll, edit_id, new_w)
            if modified:
                st.success("Gewicht aktualisiert.")
                load_data.clear()
            else:
                st.warning("Keine Änderung vorgenommen.")
    else:
        st.info("Noch keine Einträge zum Bearbeiten.")

# Hauptbereich: Tabelle & Diagramm
col1, col2 = st.columns(2)
with col1:
    st.subheader("Aktuelle Einträge")
    show_sport = st.checkbox("Nur mit Sport", key="filter_sport")
    df_view = df[df["sports_activity"] == "Yes"] if show_sport else df
    st.dataframe(df_view)

with col2:
    if not df.empty:
        df_chart = df.copy().set_index("date")
        df_chart["7d_avg"] = df_chart["weight"].rolling(window=7).mean()
        fig = px.line(
            df_chart.reset_index(),
            x="date", y=["weight", "7d_avg"],
            title="Gewicht & 7‑Tage‑Durchschnitt",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Kein Diagramm anzuzeigen.")

# Manuelles Refresh
if st.button("Daten aktualisieren", key="refresh"):
    load_data.clear()
    st.rerun()

# .streamlit/secrets.toml Beispiel
# [default]
# MONGO_URI = "mongodb+srv://user:password@whcluster0.kxjuhm0.mongodb.net/weight_tracker?..."
=======
>>>>>>> 6e4dcff (edit)
