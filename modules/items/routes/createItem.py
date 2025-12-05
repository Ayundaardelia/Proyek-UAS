from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from modules.items.models import WasteModel
from modules.items.schema.schemas import WasteCreate, WasteResponse

router = APIRouter(
    prefix="/waste",
    tags=["waste - create"],
)


@router.post("/", response_model=WasteResponse)
def create_waste(payload: WasteCreate, db: Session = Depends(get_db)):
    # cek apakah city_district sudah ada
    existing = (
        db.query(WasteModel)
        .filter(WasteModel.city_district == payload.city_district)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="City already exists")

    new_item = WasteModel(
        city_district=payload.city_district,
        waste_type=payload.waste_type,
        waste_generated=payload.waste_generated,
        year=payload.year,
        recycling_rate=payload.recycling_rate,
        population_density=payload.population_density,
        municipal_efficiency_score=payload.municipal_efficiency_score,
        disposal_method=payload.disposal_method,
        cost_management=payload.cost_management,
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item