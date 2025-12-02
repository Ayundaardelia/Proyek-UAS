from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from modules.items.schema.schemas import WasteCreate, WasteResponse
from modules.items.models import WasteModel 

router = APIRouter(prefix="/waste", tags=["waste"])

@router.post("/", response_model=WasteResponse)
def create_waste(item: WasteCreate, db: Session = Depends(get_db)):
    db_item = WasteModel(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item