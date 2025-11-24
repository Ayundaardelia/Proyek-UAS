import pandas as pd
from sqlalchemy import text
from database import engine

# Query ke MySQL
query = text("SELECT * FROM waste_management_and_recycling_india")

# Ambil data ke DataFrame
df = pd.read_sql(query, engine)

# Print ke terminal VSCode
print(df)