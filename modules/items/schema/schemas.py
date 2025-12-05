from pydantic import BaseModel
from typing import Optional

# ---------- Base ----------
class WasteBase(BaseModel):
    city_district: str
    waste_type: str
    waste_generated: float
    year: int
    recycling_rate: float
    population_density: Optional[int] = None
    municipal_efficiency_score: Optional[int] = None
    disposal_method: Optional[str] = None
    cost_management: Optional[float] = None


# ---------- Untuk create ----------
class WasteCreate(WasteBase):
    pass


# ---------- Untuk update (semua optional) ----------
class WasteUpdate(BaseModel):
    waste_type: Optional[str] = None
    waste_generated: Optional[float] = None
    year: Optional[int] = None
    recycling_rate: Optional[float] = None
    population_density: Optional[int] = None
    municipal_efficiency_score: Optional[int] = None
    disposal_method: Optional[str] = None
    cost_management: Optional[float] = None


# ---------- Untuk response ----------
class WasteResponse(WasteBase):
    class Config:
        from_attributes = True   # pydantic v2


# ----------------------------
# SCHEMA UNTUK ANALISIS DATA
# ----------------------------

# 1. Rata-rata volume sampah per kota
class AvgWasteByCity(BaseModel):
    city_district: str
    avg_waste_generated: float

    class Config:
        from_attributes = True


# 2. Rata-rata volume sampah per tipe
class AvgWasteByType(BaseModel):
    waste_type: str
    avg_waste_generated: float

    class Config:
        from_attributes = True


# 3. Tren total sampah per tahun
class TrendWasteByYear(BaseModel):
    year: int
    total_waste_generated: float

    class Config:
        from_attributes = True


# 4. Top kota dengan total sampah terbesar
class TopCity(BaseModel):
    city_district: str
    total_waste_generated: float

    class Config:
        from_attributes = True


# 5. Distribusi tipe sampah (total + persentase)
class WasteTypeDistribution(BaseModel):
    waste_type: str
    total_waste_generated: float
    percent: float

    class Config:
        from_attributes = True


# 6. Forecast sederhana tahun berikutnya
class WasteForecast(BaseModel):
    last_year: int
    last_total_waste: float
    prev_year: int
    prev_total_waste: float
    forecast_year: int
    forecast_total_waste: float
    method: str