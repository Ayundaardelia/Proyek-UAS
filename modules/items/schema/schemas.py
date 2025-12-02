from pydantic import BaseModel
from typing import Optional

class WasteBase(BaseModel):
    city_district: Optional[str] = None
    waste_type: Optional[str] = None
    waste_generated: Optional[float] = None
    recycling_rate: Optional[float] = None
    population_density: Optional[int] = None
    municipal_efficiency_score: Optional[int] = None
    disposal_method: Optional[str] = None
    cost_management: Optional[float] = None

class WasteCreate(WasteBase):
    # semua field dari WasteBase opsional → bisa create partial data
    pass

class WasteUpdate(WasteBase):
    # update juga boleh parsial, exclude_unset diambil hanya yang diisi
    pass

class WasteResponse(WasteBase):
    id: int

    class Config:
        orm_mode = True


# ==== TAMBAHKAN BAGIAN ANALISIS DI BAWAH INI ====

class AvgWasteByCity(BaseModel):
    city_district: str
    avg_waste_generated: float

class AvgWasteByType(BaseModel):
    waste_type: str
    avg_waste_generated: float

class TopCity(BaseModel):
    city_district: str
    total_waste_generated: float

class WasteTypeDistribution(BaseModel):
    waste_type: str
    total_waste_generated: float
    percentage: float