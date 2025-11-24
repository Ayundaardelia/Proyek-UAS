from sqlalchemy import Column, Integer, String, Float
from database import Base

class WasteModel(Base):
    __tablename__ = "waste_management_and_recycling_india"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_district = Column("City/District", String(255))
    waste_type = Column("Waste Type", String(255))
    waste_generated = Column("Waste Generated (Tons/Day)", Float)
    recycling_rate = Column("Recycling Rate (%)", Float)
    population_density = Column("Population Density (People/kmÂ²)", Integer)
    municipal_efficiency_score = Column("Municipal Efficiency Score (1-10)", Integer)
    disposal_method = Column("Disposal Method", String(255))
    cost_management = Column("Cost of Waste Management (â‚¹/Ton)", Float)