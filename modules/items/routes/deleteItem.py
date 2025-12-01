from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from modules.items.models import WasteModel


router = APIRouter(prefix="/waste", tags=["waste"])

@router.delete("/{id}")
def delete_waste(id: int, db: Session = Depends(get_db)):
    data = db.query(WasteModel).filter(WasteModel.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan")

    db.delete(data)
    db.commit()
    return {"detail": "Data berhasil dihapus"}