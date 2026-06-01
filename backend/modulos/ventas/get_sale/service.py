
from fastapi import HTTPException
from shared.database import get_connection

from .repository import get_sale_by_id,get_sales
from .schemas import SaleResponse

#-------------------
# Funciones
#-------------------
# Mapeo de la venta
def map_sale(row):
  return SaleResponse(
    id=row["id"],
    sold_at=row["sold_at"],
    total_amount=row["total_amount"]
  )

# Una sola venta
def execute_get_sale(sale_id: int):
  conn = get_connection()
  try:
    row = get_sale_by_id(conn, sale_id)
    if row is None:
      raise HTTPException(
        status_code=404,
        detail="Venta no encontrada"
      )
    return map_sale(row)
  finally:
    conn.close()


# Lista de ventas
def execute_get_sales():
  conn = get_connection()
  try:
    rows = get_sales(conn)
    sales_list = [map_sale(row) for row in rows]
    return sales_list

  finally:
    conn.close()
