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


@router.get("/{id}", response_model=WasteResponse)
def get_one(id: int, db: Session = Depends(get_db)):
    item = db.query(WasteModel).filter(WasteModel.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan")
    return item
