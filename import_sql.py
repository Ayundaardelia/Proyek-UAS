import pandas as pd
from sqlalchemy import text
from pathlib import Path
from database import engine

# 0. SETUP PATH PENYIMPANAN CSV
BASE_DIR = Path(__file__).resolve().parent        # folder tempat import_sql.py
ROUTES_DIR = BASE_DIR / "modules" / "items" / "routes"
ROUTES_DIR.mkdir(parents=True, exist_ok=True)     # kalau belum ada, dibuat otomatis

RAW_CSV_PATH = ROUTES_DIR / "waste_data_raw.csv"
PROCESSED_CSV_PATH = ROUTES_DIR / "waste_data_processed.csv"

# 1. IMPORT DATA DARI SQL → DATAFRAME
query = text("SELECT * FROM waste_management_and_recycling_india")
df = pd.read_sql(query, engine)

# simpan data mentah ke CSV di folder routes
df.to_csv(RAW_CSV_PATH, index=False)
print("✅ Data RAW berhasil diexport ke:", RAW_CSV_PATH)
print("Total rows:", len(df))

print("\n======= 5 DATA PERTAMA (RAW) =======")
print(df.head(5).to_string())

print("\n======= 5 DATA TERAKHIR (RAW) =======")
print(df.tail(5).to_string())

# 2. CLEANING + FEATURE ENGINEERING (OPSIONAL)
#    HANYA JALAN KALAU KOLUMNYA ADA
needed_cols = {"location", "waste_type", "date", "volume"}

if needed_cols.issubset(df.columns):
    print("\n🔧 Kolom analisis lengkap ditemukan, mulai proses cleaning & feature engineering...")

    # pastikan kolom tanggal bertipe datetime
    df["date"] = pd.to_datetime(df["date"])

    # --- Cleaning dasar ---
    # hapus duplikat berdasarkan ke-4 kolom utama
    df = df.drop_duplicates(subset=["location", "waste_type", "date", "volume"])

    # hapus baris yang nilai pentingnya kosong
    df = df.dropna(subset=["location", "waste_type", "date", "volume"])

    # volume tidak boleh negatif
    df = df[df["volume"] >= 0]

    # buang volume yang tidak realistis (>10.000 misal)
    df = df[df["volume"] <= 10000]

    # --- Feature Engineering: variabel waktu ---
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["weekday"] = df["date"].dt.day_name()
    df["week_of_year"] = df["date"].dt.isocalendar().week

    # --- Rolling mean 7 hari per lokasi & jenis ---
    df = df.sort_values(["location", "waste_type", "date"])
    df["volume_7d_mean"] = (
        df.groupby(["location", "waste_type"])["volume"]
          .transform(lambda s: s.rolling(window=7, min_periods=1).mean())
    )

    # simpan hasil processed
    df.to_csv(PROCESSED_CSV_PATH, index=False)
    print("\n📦 Data PROCESSED disimpan ke:", PROCESSED_CSV_PATH)
    print("Total rows setelah cleaning:", len(df))

    print("\n======= 5 DATA PERTAMA (PROCESSED) =======")
    print(df.head(5).to_string())

    print("\n======= 5 DATA TERAKHIR (PROCESSED) =======")
    print(df.tail(5).to_string())

else:
    print("\n⚠ Kolom 'location', 'waste_type', 'date', 'volume' belum lengkap di tabel SQL.")
    print("   Jadi untuk sekarang hanya export RAW CSV saja tanpa cleaning & feature engineering.")
    print("   Kolom yang tersedia saat ini:", list(df.columns))