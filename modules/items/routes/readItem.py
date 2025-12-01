from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from modules.items.schema.schemas import WasteResponse
from modules.items.models import WasteModel

router = APIRouter(prefix="/waste", tags=["waste"])

@router.get("/", response_model=List[WasteResponse])
def get_all(db: Session = Depends(get_db)):
    return db.query(WasteModel).all()

@router.get("/{id}", response_model=WasteResponse)
def get_one(id: int, db: Session = Depends(get_db)):
    item = db.query(WasteModel).filter(WasteModel.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan")
    return item