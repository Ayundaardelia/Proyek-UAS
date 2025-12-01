from pydantic import BaseModel

class WasteBase(BaseModel):
    city_district: str
    waste_type: str
    waste_generated: float
    recycling_rate: float
    population_density: int
    municipal_efficiency_score: int
    disposal_method: str
    cost_management: float

class WasteCreate(WasteBase):
    pass

class WasteUpdate(BaseModel):
    city_district: str | None = None
    waste_type: str | None = None
    waste_generated: float | None = None
    recycling_rate: float | None = None
    population_density: int | None = None
    municipal_efficiency_score: int | None = None
    disposal_method: str | None = None
    cost_management: float | None = None

class WasteOut(WasteBase):
    id: int

    class Config:
        orm_mode = True
