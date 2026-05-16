import sqlite3
import os

# ==========================================
# CREATE DATA FOLDER
# ==========================================

os.makedirs(
    "data",
    exist_ok=True
)

# ==========================================
# DATABASE CONNECTION
# ==========================================

conn = sqlite3.connect(
    "data/ocr_database.db",
    check_same_thread=False
)

cursor = conn.cursor()

# ==========================================
# CREATE TABLES
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS excel_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    google_sheet_url TEXT,

    excel_name TEXT,

    total_records INTEGER,

    created_at TEXT

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ocr_records (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    excel_history_id INTEGER,

    image_name TEXT,

    image_data BLOB,

    extracted_text TEXT,

    source_type TEXT,

    image_url TEXT,

    created_at TEXT

)
""")

conn.commit()