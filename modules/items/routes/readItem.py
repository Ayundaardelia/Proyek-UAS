from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from modules.items.models import WasteModel
from modules.items.schema.schemas import WasteResponse

router = APIRouter(
    prefix="/waste",
    tags=["waste - read"],
)


@router.get("/", response_model=list[WasteResponse])
def get_all_waste(db: Session = Depends(get_db)):
    data = db.query(WasteModel).all()
    return data


@router.get("/{city_district}", response_model=WasteResponse)
def get_one_waste(city_district: str, db: Session = Depends(get_db)):
    data = (
        db.query(WasteModel)
        .filter(WasteModel.city_district == city_district)
        .first()
    )
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data