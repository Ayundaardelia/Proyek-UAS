from sqlalchemy import Column, Integer, String, Float
from database import Base


class WasteModel(Base):
    __tablename__ = "waste_management_and_recycling_india"

    # Pakai City_District sebagai primary key (cukup untuk baca/analytics)
    city_district = Column("City_District", String(255), primary_key=True)

    waste_type = Column("Waste_Type", String(255))
    waste_generated = Column("Waste_Generated_Tons_Day", Float)
    recycling_rate = Column("Recycling_Rate", Float)
    population_density = Column("Population_Density_People_km2", Integer)
    municipal_efficiency_score = Column("Municipal_Efficiency_Score", Integer)
    disposal_method = Column("Disposal_Method", String(255))
    cost_management = Column("Cost_of_Waste_Management_Rs_Per_Ton", Float)
    year = Column("Year", Integer)