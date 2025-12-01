from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from modules.items.schema.schemas import WasteUpdate, WasteOut
from modules.items.transactions.models import WasteModel
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.put("/waste/{id}", response_model=WasteOut)
def update_waste(id: int, payload: WasteUpdate, db: Session = Depends(get_db)):
    data = db.query(WasteModel).filter(WasteModel.id == id).first()
    if not data:
        raise HTTPException(404, "Data not found")

    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(data, key, value)

    db.commit()
    db.refresh(data)
    return data
