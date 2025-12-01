from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from modules.items.schema.schemas import WasteOut
from modules.items.transactions.models import WasteModel
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/waste", response_model=list[WasteOut])
def get_all_waste(db: Session = Depends(get_db)):
    return db.query(WasteModel).all()

@router.get("/waste/{id}", response_model=WasteOut)
def get_waste(id: int, db: Session = Depends(get_db)):
    waste = db.query(WasteModel).filter(WasteModel.id == id).first()
    if not waste:
        raise HTTPException(404, "Data not found")
    return waste
