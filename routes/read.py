from fastapi import APIRouter
from typing import List
from database import get_db_connection

# Membuat router untuk mengatur endpoint API
router = APIRouter()


@router.get("/data", response_model=List[dict], tags=["CRUD"])
def read_all_data():
    # Mengambil semua data dari tabel waste_management
    conn = get_db_connection()           # Membuka koneksi ke database
    cursor = conn.cursor()               # Membuat cursor untuk eksekusi query
    cursor.execute("SELECT * FROM waste_management")  # Query untuk ambil semua data
    rows = cursor.fetchall()             # Mengambil semua hasil query
    conn.close()                         # Menutup koneksi database
    return [dict(row) for row in rows]   # Mengembalikan hasil dalam bentuk list of dict


@router.get("/data/{item_id}", tags=["CRUD"])
def read_item(item_id: int):
    from fastapi import HTTPException

    # Mengambil data berdasarkan ID tertentu
    conn = get_db_connection()                           # Membuka koneksi ke database
    cursor = conn.cursor()                               # Membuat cursor
    cursor.execute("SELECT * FROM waste_management WHERE id = ?", (item_id,))  # Query dengan parameter ID
    row = cursor.fetchone()                              # Mengambil satu baris data
    conn.close()                                         # Menutup koneksi database
    if row is None:                                      # Jika data tidak ditemukan
        raise HTTPException(status_code=404, detail="Item not found")  # Kembalikan error 404
    return dict(row)                                     # Mengembalikan data dalam bentuk dictionary
