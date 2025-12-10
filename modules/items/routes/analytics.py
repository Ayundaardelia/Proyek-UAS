from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from modules.items import models
from modules.items.schema import schemas

router = APIRouter(
    prefix="/waste",
    tags=["waste - analytics"],
)

# 1. RATA-RATA VOLUME SAMPAH PER KOTA/DAERAH
@router.get("/avg-by-city", response_model=List[schemas.AvgWasteByCity])
def avg_waste_by_city(db: Session = Depends(get_db)):
    rows = (
        db.query(
            models.WasteModel.city_district.label("city_district"),
            func.avg(models.WasteModel.waste_generated).label("avg_waste_generated"),
        )
        .group_by(models.WasteModel.city_district)
        .all()
    )

    return [
        schemas.AvgWasteByCity(
            city_district=r.city_district,
            avg_waste_generated=float(r.avg_waste_generated or 0.0),
        )
        for r in rows
    ]


# 2. RATA-RATA VOLUME SAMPAH PER TIPE SAMPAH
@router.get("/avg-by-type", response_model=List[schemas.AvgWasteByType])
def avg_waste_by_type(db: Session = Depends(get_db)):
    rows = (
        db.query(
            models.WasteModel.waste_type.label("waste_type"),
            func.avg(models.WasteModel.waste_generated).label("avg_waste_generated"),
        )
        .group_by(models.WasteModel.waste_type)
        .all()
    )

    return [
        schemas.AvgWasteByType(
            waste_type=r.waste_type,
            avg_waste_generated=float(r.avg_waste_generated or 0.0),
        )
        for r in rows
    ]


# 3. TREN TOTAL SAMPAH PER TAHUN (SUM)
@router.get("/trend-year", response_model=List[schemas.TrendWasteByYear])
def trend_waste_per_year(db: Session = Depends(get_db)):
    rows = (
        db.query(
            models.WasteModel.year.label("year"),
            func.sum(models.WasteModel.waste_generated).label("total_waste_generated"),
        )
        .group_by(models.WasteModel.year)
        .order_by(models.WasteModel.year)
        .all()
    )

    return [
        schemas.TrendWasteByYear(
            year=int(r.year),
            total_waste_generated=float(r.total_waste_generated or 0.0),
        )
        for r in rows
    ]


# 4. TOP N KOTA DENGAN TOTAL SAMPAH TERBESAR
@router.get("/top-city", response_model=List[schemas.TopCity])
def top_city_by_waste(n: int = 5, db: Session = Depends(get_db)):
    rows = (
        db.query(
            models.WasteModel.city_district.label("city_district"),
            func.sum(models.WasteModel.waste_generated).label("total_waste_generated"),
        )
        .group_by(models.WasteModel.city_district)
        .order_by(func.sum(models.WasteModel.waste_generated).desc())
        .limit(n)
        .all()
    )

    return [
        schemas.TopCity(
            city_district=r.city_district,
            total_waste_generated=float(r.total_waste_generated or 0.0),
        )
        for r in rows
    ]


# 5. DISTRIBUSI TIPE SAMPAH (TOTAL + PERSENTASE)
@router.get("/type-distribution", response_model=List[schemas.WasteTypeDistribution])
def type_distribution(db: Session = Depends(get_db)):
    rows = (
        db.query(
            models.WasteModel.waste_type.label("waste_type"),
            func.sum(models.WasteModel.waste_generated).label("total_waste_generated"),
        )
        .group_by(models.WasteModel.waste_type)
        .all()
    )

    # total semua jenis, buat hitung persentase
    grand_total = sum(float(r.total_waste_generated or 0.0) for r in rows) or 1.0

    result = []
    for r in rows:
        total = float(r.total_waste_generated or 0.0)
        percent = (total / grand_total) * 100.0

        result.append(
            schemas.WasteTypeDistribution(
                waste_type=r.waste_type,
                total_waste_generated=total,
                percent=percent,
            )
        )

    return result


# 6. FORECAST SEDERHANA TAHUN BERIKUTNYA
@router.get("/forecast-next-year", response_model=schemas.WasteForecast)
def forecast_next_year(db: Session = Depends(get_db)):
    # total sampah per tahun
    rows = (
        db.query(
            models.WasteModel.year.label("year"),
            func.sum(models.WasteModel.waste_generated).label("total_waste_generated"),
        )
        .group_by(models.WasteModel.year)
        .order_by(models.WasteModel.year)
        .all()
    )

    if not rows or len(rows) < 2:
        raise HTTPException(
            status_code=400,
            detail="Data tahun tidak cukup untuk membuat forecast sederhana.",
        )

    last = rows[-1]
    prev = rows[-2]

    last_total = float(last.total_waste_generated or 0.0)
    prev_total = float(prev.total_waste_generated or 0.0)

    growth = last_total - prev_total  # selisih sederhana

    forecast_year = int(last.year) + 1
    forecast_total = max(last_total + growth, 0.0)

    return schemas.WasteForecast(
        year=forecast_year,
        predicted_total_waste=forecast_total,
    )