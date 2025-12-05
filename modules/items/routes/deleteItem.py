from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from modules.items.models import WasteModel

router = APIRouter(
    prefix="/waste",
    tags=["waste - delete"],
)


@router.delete("/{city_district}")
def delete_waste(city_district: str, db: Session = Depends(get_db)):
    item = (
        db.query(WasteModel)
        .filter(WasteModel.city_district == city_district)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Data not found")

    db.delete(item)
    db.commit()
    return {"detail": "Deleted"}