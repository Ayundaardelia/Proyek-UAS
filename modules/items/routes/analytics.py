from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from database import get_db
from modules.items.schema.models import WasteModel
from modules.items.schema import schemas

router = APIRouter(prefix="/analytics", tags=["analytics"])


# 1) Rata-rata volume sampah per kota
@router.get("/avg-by-city", response_model=List[schemas.AvgWasteByCity])
def avg_waste_by_city(db: Session = Depends(get_db)):
    rows = (
        db.query(
            WasteModel.city_district.label("city_district"),
            func.avg(WasteModel.waste_generated).label("avg_waste_generated"),
        )
        .group_by(WasteModel.city_district)
        .all()
    )
    return [
        schemas.AvgWasteByCity(
            city_district=r.city_district,
            avg_waste_generated=r.avg_waste_generated or 0.0,
        )
        for r in rows
    ]


# 2) Rata-rata volume sampah per jenis sampah
@router.get("/avg-by-type", response_model=List[schemas.AvgWasteByType])
def avg_waste_by_type(db: Session = Depends(get_db)):
    rows = (
        db.query(
            WasteModel.waste_type.label("waste_type"),
            func.avg(WasteModel.waste_generated).label("avg_waste_generated"),
        )
        .group_by(WasteModel.waste_type)
        .all()
    )
    return [
        schemas.AvgWasteByType(
            waste_type=r.waste_type,
            avg_waste_generated=r.avg_waste_generated or 0.0,
        )
        for r in rows
    ]


# 3) Kota dengan produksi sampah tertinggi (bisa top N)
@router.get("/top-cities", response_model=List[schemas.TopCity])
def top_cities(limit: int = 10, db: Session = Depends(get_db)):
    rows = (
        db.query(
            WasteModel.city_district.label("city_district"),
            func.sum(WasteModel.waste_generated).label("total_waste_generated"),
        )
        .group_by(WasteModel.city_district)
        .order_by(func.sum(WasteModel.waste_generated).desc())
        .limit(limit)
        .all()
    )
    return [
        schemas.TopCity(
            city_district=r.city_district,
            total_waste_generated=r.total_waste_generated or 0.0,
        )
        for r in rows
    ]


# 4) Distribusi jenis sampah (total & persentase)
@router.get(
    "/waste-type-distribution",
    response_model=List[schemas.WasteTypeDistribution],
)
def waste_type_distribution(db: Session = Depends(get_db)):
    # total semua sampah
    total_all = (
        db.query(func.sum(WasteModel.waste_generated))
        .scalar()
        or 0.0
    )

    rows = (
        db.query(
            WasteModel.waste_type.label("waste_type"),
            func.sum(WasteModel.waste_generated).label("total_waste_generated"),
        )
        .group_by(WasteModel.waste_type)
        .all()
    )

    result = []
    for r in rows:
        total = r.total_waste_generated or 0.0
        pct = (total / total_all * 100) if total_all > 0 else 0.0
        result.append(
            schemas.WasteTypeDistribution(
                waste_type=r.waste_type,
                total_waste_generated=total,
                percentage=pct,
            )
        )
    return result