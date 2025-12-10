import sqlite3
import pandas as pd
import os
from config import DB_NAME, CSV_FILE


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS waste_management (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_district TEXT,
            waste_type TEXT,
            waste_generated_tons_per_day REAL,
            recycling_rate_percent REAL,
            population_density REAL,
            municipal_efficiency_score INTEGER,
            disposal_method TEXT,
            cost_per_ton REAL,
            awareness_campaigns_count INTEGER,
            landfill_name TEXT,
            landfill_location TEXT,
            landfill_capacity_tons REAL,
            year INTEGER
        )
    """
    )

    cursor.execute("SELECT count(*) FROM waste_management")
    count = cursor.fetchone()[0]

    if count == 0 and os.path.exists(CSV_FILE):
        print("Database kosong. Melakukan import dari dataset.csv...")
        try:
            df = pd.read_csv(CSV_FILE)

            column_mapping = {
                "City/District": "city_district",
                "Waste Type": "waste_type",
                "Waste Generated (Tons/Day)": "waste_generated_tons_per_day",
                "Recycling Rate (%)": "recycling_rate_percent",
                "Population Density (People/km²)": "population_density",
                "Municipal Efficiency Score (1-10)": "municipal_efficiency_score",
                "Disposal Method": "disposal_method",
                "Cost of Waste Management (₹/Ton)": "cost_per_ton",
                "Awareness Campaigns Count": "awareness_campaigns_count",
                "Landfill Name": "landfill_name",
                "Landfill Location (Lat, Long)": "landfill_location",
                "Landfill Capacity (Tons)": "landfill_capacity_tons",
                "Year": "year",
            }

            df = df.rename(columns=column_mapping)
            df.to_sql("waste_management", conn, if_exists="append", index=False)
            print("Import berhasil!")
        except Exception as e:
            print(f"Gagal import CSV: {e}")

    conn.commit()
    conn.close()
