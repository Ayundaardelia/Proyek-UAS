import pandas as pd
from sqlalchemy import text
from database import engine

# Query dari SQL
query = text("SELECT * FROM waste_management_and_recycling_india")

# Load ke DataFrame
df = pd.read_sql(query, engine)

# Export ke CSV
df.to_csv("waste_data_export.csv", index=False)

print("✅ Data berhasil diexport ke waste_data_export.csv")

print("======= 5 DATA PERTAMA =======")
print(df.head(5).to_string())

print("\n======= 5 DATA TERAKHIR =======")
print(df.tail(5).to_string())python import_sql.py
