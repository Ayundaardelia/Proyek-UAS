from pydantic import BaseModel

# ---------- Base ----------
class WasteBase(BaseModel):
    city_district: str
    waste_type: str
    waste_generated: float
    year: int
    recycling_rate: float
    population_density: int | None = None
    municipal_efficiency_score: int | None = None
    disposal_method: str | None = None
    cost_management: float | None = None


# ---------- Untuk create ----------
class WasteCreate(WasteBase):
    pass


# ---------- Untuk update (semua optional) ----------
class WasteUpdate(BaseModel):
    waste_type: str | None = None
    waste_generated: float | None = None
    year: int | None = None
    recycling_rate: float | None = None
    population_density: int | None = None
    municipal_efficiency_score: int | None = None
    disposal_method: str | None = None
    cost_management: float | None = None


# ---------- Untuk response ----------
class WasteResponse(WasteBase):
    class Config:
        from_attributes = True  # pydantic v2
        # kalau kamu masih pakai v1, ganti jadi: orm_mode = True