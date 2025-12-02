from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from modules.items.models import WasteModel
from modules.items.schema import schemas

router = APIRouter(prefix="/analytics", tags=["analytics"])


def _safe_float(value) -> float:
    """Konversi None ke 0.0, selain itu ke float biasa."""
    return float(value or 0.0)


# 1) Rata-rata volume sampah per kota
@router.get("/avg-by-city", response_model=list[schemas.AvgWasteByCity])
def avg_waste_by_city(db: Session = Depends(get_db)) -> list[schemas.AvgWasteByCity]:
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
            city_district=row.city_district,
            avg_waste_generated=_safe_float(row.avg_waste_generated),
        )
        for row in rows
    ]


# 2) Rata-rata volume sampah per jenis sampah
@router.get("/avg-by-type", response_model=list[schemas.AvgWasteByType])
def avg_waste_by_type(db: Session = Depends(get_db)) -> list[schemas.AvgWasteByType]:
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
            waste_type=row.waste_type,
            avg_waste_generated=_safe_float(row.avg_waste_generated),
        )
        for row in rows
    ]


# 3) Kota dengan produksi sampah tertinggi (bisa top N)
@router.get("/top-cities", response_model=list[schemas.TopCity])
def top_cities(
    limit: int = 10,
    db: Session = Depends(get_db),
) -> list[schemas.TopCity]:
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
            city_district=row.city_district,
            total_waste_generated=_safe_float(row.total_waste_generated),
        )
        for row in rows
    ]


# 4) Distribusi jenis sampah (total & persentase)
@router.get(
    "/waste-type-distribution",
    response_model=list[schemas.WasteTypeDistribution],
)
def waste_type_distribution(
    db: Session = Depends(get_db),
) -> list[schemas.WasteTypeDistribution]:
    # total seluruh sampah
    total_all = _safe_float(
        db.query(func.sum(WasteModel.waste_generated)).scalar()
    )

    rows = (
        db.query(
            WasteModel.waste_type.label("waste_type"),
            func.sum(WasteModel.waste_generated).label("total_waste_generated"),
        )
        .group_by(WasteModel.waste_type)
        .all()
    )

    result: list[schemas.WasteTypeDistribution] = []
    for row in rows:
        total = _safe_float(row.total_waste_generated)
        percentage = (total / total_all * 100) if total_all > 0 else 0.0

        result.append(
            schemas.WasteTypeDistribution(
                waste_type=row.waste_type,
                total_waste_generated=total,
                percentage=percentage,
            )
        )
    return result