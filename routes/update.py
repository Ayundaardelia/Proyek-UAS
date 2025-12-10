from fastapi import APIRouter, HTTPException
from models import WasteDataUpdate
from database import get_db_connection

# Membuat router untuk endpoint CRUD
router = APIRouter()


@router.put("/data/{item_id}", tags=["CRUD"])
def update_item(item_id: int, item: WasteDataUpdate):
    # Mengubah (update) data sampah berdasarkan ID
    conn = get_db_connection()                     # Membuka koneksi ke database
    cursor = conn.cursor()                         # Membuat cursor untuk menjalankan query

    update_data = item.dict(exclude_unset=True)    # Mengambil hanya field yang dikirim oleh user

    # Jika tidak ada data yang diberikan untuk diupdate
    if not update_data:
        conn.close()                               # Tutup koneksi
        raise HTTPException(status_code=400, detail="No data provided for update")  # Kembalikan error 400

    # Menyusun bagian SET dari query SQL secara dinamis
    set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])
    values = list(update_data.values())            # Nilai baru untuk update
    values.append(item_id)                         # Tambahkan ID ke akhir list untuk klausa WHERE

    # Eksekusi query UPDATE dengan parameter dinamis
    cursor.execute(f"UPDATE waste_management SET {set_clause} WHERE id = ?", values)
    conn.commit()                                  # Simpan perubahan ke database

    # Jika tidak ada baris yang diubah, berarti ID tidak ditemukan
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Item not found")

    conn.close()                                   # Tutup koneksi database
    return {"message": "Item updated successfully"} # Kembalikan pesan sukses jika update berhasil
