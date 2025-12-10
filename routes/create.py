from fastapi import APIRouter, HTTPException
from models import WasteData
from database import get_db_connection

router = APIRouter()


@router.post("/data", status_code=201, tags=["CRUD"])
def create_item(item: WasteData):
    conn = get_db_connection()
    cursor = conn.cursor()

    check_query = """
    SELECT id FROM waste_management 
    WHERE city_district = ? AND waste_type = ? AND year = ?
    """
    cursor.execute(check_query, (item.city_district, item.waste_type, item.year))
    existing = cursor.fetchone()

    if existing:
        conn.close()
        raise HTTPException(
            status_code=409,
            detail=f"Data already exists for {item.city_district}, {item.waste_type}, year {item.year}",
        )

    query = """
    INSERT INTO waste_management (
        city_district, waste_type, waste_generated_tons_per_day, recycling_rate_percent,
        population_density, municipal_efficiency_score, disposal_method, cost_per_ton,
        awareness_campaigns_count, landfill_name, landfill_location, landfill_capacity_tons, year
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    values = (
        item.city_district,
        item.waste_type,
        item.waste_generated_tons_per_day,
        item.recycling_rate_percent,
        item.population_density,
        item.municipal_efficiency_score,
        item.disposal_method,
        item.cost_per_ton,
        item.awareness_campaigns_count,
        item.landfill_name,
        item.landfill_location,
        item.landfill_capacity_tons,
        item.year,
    )

    cursor.execute(query, values)
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, "message": "Item created successfully"}
