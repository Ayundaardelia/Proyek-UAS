from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from modules.items.schema.schemas import WasteUpdate, WasteResponse
from modules.items.schema.models import WasteModel

router = APIRouter(prefix="/waste", tags=["waste"])

@router.put("/{id}", response_model=WasteResponse)
def update_waste(id: int, item: WasteUpdate, db: Session = Depends(get_db)):
    data = db.query(WasteModel).filter(WasteModel.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan")

    update_data = item.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(data, key, value)

    db.commit()
    db.refresh(data)
    return data