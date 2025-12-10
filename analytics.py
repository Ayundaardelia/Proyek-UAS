from fastapi import APIRouter
from database import get_db_connection

router = APIRouter()


@router.get("/analysis/average-volume", tags=["Analysis"])
def get_average_volume():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT city_district, waste_type, AVG(waste_generated_tons_per_day) as average_tonnage
        FROM waste_management 
        GROUP BY city_district, waste_type
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.get("/analysis/trend", tags=["Analysis"])
def get_waste_trend():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT year, SUM(waste_generated_tons_per_day) as total_tonnage
        FROM waste_management 
        GROUP BY year 
        ORDER BY year ASC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.get("/analysis/highest-production-location", tags=["Analysis"])
def get_highest_production():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT city_district, SUM(waste_generated_tons_per_day) as total_waste
        FROM waste_management 
        GROUP BY city_district 
        ORDER BY total_waste DESC 
        LIMIT 5
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.get("/analysis/waste-distribution", tags=["Analysis"])
def get_waste_distribution():
    conn = get_db_connection()
    cursor = conn.cursor()

    query_total = "SELECT SUM(waste_generated_tons_per_day) FROM waste_management"
    cursor.execute(query_total)
    total_waste = cursor.fetchone()[0] or 1

    query = """
        SELECT waste_type, SUM(waste_generated_tons_per_day) as type_total
        FROM waste_management 
        GROUP BY waste_type
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        data = dict(row)
        data["percentage"] = round((data["type_total"] / total_waste) * 100, 2)
        result.append(data)

    return result


@router.get("/analysis/prediction", tags=["Analysis"])
def predict_waste_volume():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT year, SUM(waste_generated_tons_per_day) as total_waste
        FROM waste_management 
        GROUP BY year 
        ORDER BY year ASC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    data = [dict(row) for row in rows]

    if len(data) < 2:
        return {
            "message": "Data tidak cukup untuk prediksi tren (minimal 2 tahun data).",
            "current_data": data,
        }

    n = len(data)
    sum_x = sum(item["year"] for item in data)
    sum_y = sum(item["total_waste"] for item in data)
    sum_xy = sum(item["year"] * item["total_waste"] for item in data)
    sum_x2 = sum(item["year"] ** 2 for item in data)

    slope = (
        (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
        if (n * sum_x2 - sum_x**2) != 0
        else 0
    )
    intercept = (sum_y - slope * sum_x) / n

    last_year = data[-1]["year"]
    next_year = last_year + 1
    predicted_value = slope * next_year + intercept

    return {
        "historical_data": data,
        "prediction_year": next_year,
        "predicted_total_waste_tons": round(predicted_value, 2),
        "note": "Prediksi menggunakan regresi linier sederhana berdasarkan data tahunan.",
    }
