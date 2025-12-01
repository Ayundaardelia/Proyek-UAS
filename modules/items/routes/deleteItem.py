from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from modules.items.transactions.models import WasteModel
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.delete("/waste/{id}")
def delete_waste(id: int, db: Session = Depends(get_db)):
    data = db.query(WasteModel).filter(WasteModel.id == id).first()
    if not data:
        raise HTTPException(404, "Data not found")

    db.delete(data)
    db.commit()
    return {"message": "Data deleted successfully"}
