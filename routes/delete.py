from fastapi import APIRouter, HTTPException
from database import get_db_connection

# Membuat router untuk endpoint CRUD
router = APIRouter()


@router.delete("/data/{item_id}", tags=["CRUD"])
def delete_item(item_id: int):
    # Menghapus data berdasarkan ID dari tabel waste_management
    conn = get_db_connection()                             # Membuka koneksi ke database
    cursor = conn.cursor()                                 # Membuat cursor untuk eksekusi query
    cursor.execute("DELETE FROM waste_management WHERE id = ?", (item_id,))  # Menjalankan query DELETE
    conn.commit()                                          # Menyimpan perubahan ke database

    if cursor.rowcount == 0:                               # Jika tidak ada baris yang terhapus
        conn.close()                                       # Tutup koneksi
        raise HTTPException(status_code=404, detail="Item not found")  # Kembalikan error 404 jika ID tidak ditemukan

    conn.close()                                           # Tutup koneksi database
    return {"message": "Item deleted successfully"}         # Kembalikan pesan sukses jika data berhasil dihapus
