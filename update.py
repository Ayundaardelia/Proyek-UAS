from fastapi import APIRouter, HTTPException
from models import WasteDataUpdate
from database import get_db_connection

router = APIRouter()


@router.put("/data/{item_id}", tags=["CRUD"])
def update_item(item_id: int, item: WasteDataUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()

    update_data = item.dict(exclude_unset=True)

    if not update_data:
        conn.close()
        raise HTTPException(status_code=400, detail="No data provided for update")

    set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])
    values = list(update_data.values())
    values.append(item_id)

    cursor.execute(f"UPDATE waste_management SET {set_clause} WHERE id = ?", values)
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Item not found")

    conn.close()
    return {"message": "Item updated successfully"}
