from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from modules.items.schema.schemas import ItemCreate, ItemOut
from modules.items.transactions.models import WasteModel
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/waste", response_model=WasteOut)
def create_waste(data: WasteCreate, db: Session = Depends(get_db)):
    db_item = WasteModel(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
