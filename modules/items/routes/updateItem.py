from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from modules.items.models import WasteModel
from modules.items.schema.schemas import WasteUpdate, WasteResponse

router = APIRouter(
    prefix="/waste",
    tags=["waste - update"],
)


@router.put("/{city_district}", response_model=WasteResponse)
def update_waste(
    city_district: str,
    payload: WasteUpdate,
    db: Session = Depends(get_db),
):
    item = (
        db.query(WasteModel)
        .filter(WasteModel.city_district == city_district)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Data not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item