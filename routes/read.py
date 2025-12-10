from fastapi import APIRouter
from typing import List
from database import get_db_connection

router = APIRouter()


@router.get("/data", response_model=List[dict], tags=["CRUD"])
def read_all_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM waste_management")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.get("/data/{item_id}", tags=["CRUD"])
def read_item(item_id: int):
    from fastapi import HTTPException

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM waste_management WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return dict(row)
