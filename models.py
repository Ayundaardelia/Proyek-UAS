from pydantic import BaseModel
from typing import Optional


class WasteData(BaseModel):
    city_district: str
    waste_type: str
    waste_generated_tons_per_day: float
    recycling_rate_percent: float
    population_density: float
    municipal_efficiency_score: int
    disposal_method: str
    cost_per_ton: float
    awareness_campaigns_count: int
    landfill_name: str
    landfill_location: str
    landfill_capacity_tons: float
    year: int


class WasteDataUpdate(BaseModel):
    city_district: Optional[str] = None
    waste_type: Optional[str] = None
    waste_generated_tons_per_day: Optional[float] = None
    recycling_rate_percent: Optional[float] = None
    population_density: Optional[float] = None
    municipal_efficiency_score: Optional[int] = None
    disposal_method: Optional[str] = None
    cost_per_ton: Optional[float] = None
    awareness_campaigns_count: Optional[int] = None
    landfill_name: Optional[str] = None
    landfill_location: Optional[str] = None
    landfill_capacity_tons: Optional[float] = None
    year: Optional[int] = None
