# modules/items/Analytics.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from database import get_db
from modules.items.models import WasteModel
from modules.items.schema import schemas

router = APIRouter(prefix="/analytics", tags=["analytics"])


def _safe_float(value) -> float:
    """Biar None nggak bikin error waktu di-convert ke float."""
    return float(value or 0.0)


# 1. RATA-RATA VOLUME SAMPAH PER LOKASI
#    -> menjawab: "Rata-rata volume sampah per lokasi"
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
            city_district=row.city_district,
            avg_waste_generated=_safe_float(row.avg_waste_generated),
        )
        for row in rows
    ]


# 2. RATA-RATA VOLUME SAMPAH PER JENIS SAMPAH
#    -> menjawab: "Rata-rata volume sampah per jenis sampah"
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
            waste_type=row.waste_type,
            avg_waste_generated=_safe_float(row.avg_waste_generated),
        )
        for row in rows
    ]


# 3. TREN VOLUME SAMPAH SEPANJANG WAKTU (TAHUNAN)
#    -> menjawab: "Tren volume sampah sepanjang waktu"
#    di sini kita pakai kolom Year di dataset (tren per tahun)
@router.get("/trend", response_model=List[schemas.WasteTrend])
def waste_trend(
    city: Optional[str] = None,
    waste_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(
        WasteModel.year.label("year"),
        func.sum(WasteModel.waste_generated).label("total_waste"),
    )

    if city:
        q = q.filter(WasteModel.city_district == city)
    if waste_type:
        q = q.filter(WasteModel.waste_type == waste_type)

    rows = (
        q.group_by(WasteModel.year)
        .order_by(WasteModel.year)
        .all()
    )

    return [
        schemas.WasteTrend(
            year=row.year,
            total_waste_generated=_safe_float(row.total_waste),
        )
        for row in rows
    ]


# 4. LOKASI DENGAN PRODUKSI SAMPAH TERTINGGI
#    -> menjawab: "Identifikasi lokasi dengan produksi sampah tertinggi"
@router.get("/top-cities", response_model=List[schemas.TopCity])
def top_cities(
    limit: int = 10,
    db: Session = Depends(get_db),
):
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


# 5. DISTRIBUSI JENIS SAMPAH
#    -> menjawab: "Distribusi jenis sampah"
@router.get(
    "/waste-type-distribution",
    response_model=List[schemas.WasteTypeDistribution],
)
def waste_type_distribution(db: Session = Depends(get_db)):
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

    result = []
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


# 6. PREDIKSI VOLUME SAMPAH TAHUN BERIKUTNYA
#    -> menjawab: "Prediksi volume sampah mendatang"
#    Simple linear regression (manual) berdasarkan data per tahun
def _lin_reg(x: list[int], y: list[float]) -> tuple[float, float]:
    """
    Linear regression sederhana: y = a*x + b
    return (a, b)
    """
    n = len(x)
    sx = sum(x)
    sy = sum(y)
    sxy = sum(xi * yi for xi, yi in zip(x, y))
    sx2 = sum(xi * xi for xi in x)
    denom = n * sx2 - sx * sx
    if denom == 0:
        # kalau datanya terlalu sedikit / sama semua -> fallback ke rata-rata
        return 0.0, sy / n
    a = (n * sxy - sx * sy) / denom  # slope
    b = (sy - a * sx) / n            # intercept
    return a, b


@router.get("/predict", response_model=schemas.WastePrediction)
def predict_next_year(
    city: str,
    waste_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(
        WasteModel.year.label("year"),
        func.sum(WasteModel.waste_generated).label("total_waste"),
    ).filter(WasteModel.city_district == city)

    if waste_type:
        q = q.filter(WasteModel.waste_type == waste_type)

    rows = (
        q.group_by(WasteModel.year)
        .order_by(WasteModel.year)
        .all()
    )

    if not rows:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan untuk kota tersebut")

    years = [int(r.year) for r in rows]
    totals = [_safe_float(r.total_waste) for r in rows]

    if len(years) == 1:
        # kalau cuma punya 1 tahun data, prediksi = nilai yang sama
        next_year = years[0] + 1
        pred = totals[0]
    else:
        a, b = _lin_reg(years, totals)
        next_year = max(years) + 1
        pred = a * next_year + b

    return schemas.WastePrediction(
        city_district=city,
        waste_type=waste_type,
        next_year=next_year,
        predicted_waste_generated=pred,
    )