from fastapi import APIRouter, HTTPException
from database import get_db_connection

router = APIRouter()


@router.delete("/data/{item_id}", tags=["CRUD"])
def delete_item(item_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM waste_management WHERE id = ?", (item_id,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Item not found")

    conn.close()
    return {"message": "Item deleted successfully"}