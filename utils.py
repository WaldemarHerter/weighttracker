import os
import streamlit as st             # neu importieren
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

def init_db():
    uri = os.getenv("MONGO_URI") or st.secrets["MONGO_URI"]
    if not uri:
        raise ValueError("Bitte setze MONGO_URI als Secret im Cloud‑Dashboard!")
    client = MongoClient(uri, server_api=ServerApi("1"))
    try:
        client.admin.command("ping")
        print("✅ MongoDB verbunden!")
    except Exception as e:
        raise ConnectionError(f"MongoDB‑Verbindung fehlgeschlagen: {e}")
    db = client["weight_tracker"]
    return db["weights"]

# Neuen Eintrag hinzufügen
def update_entry(collection, date: str, weight: float, sports_activity: str):
    doc = {"date": date, "weight": weight, "sports_activity": sports_activity}
    result = collection.insert_one(doc)
    return str(result.inserted_id)

# Alle Einträge abrufen

def fetch_all(collection):
    return list(collection.find().sort("date", 1))

# Eintrag löschen
def delete_entry(collection, entry_id: str):
    result = collection.delete_one({"_id": ObjectId(entry_id)})
    return result.deleted_count

# Gewicht eines Eintrags aktualisieren
def update_weight(collection, entry_id: str, new_weight: float):
    result = collection.update_one(
        {"_id": ObjectId(entry_id)},
        {"$set": {"weight": new_weight}}
    )
    return result.modified_count
