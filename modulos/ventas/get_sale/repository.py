
#-------------------------------------
# Obtención de venta por ID
#-------------------------------------
def get_sale_by_id(conn, sale_id: int):
  cursor = conn.cursor()
  cursor.execute("""
    SELECT
      id,
      sold_at,
      total_amount
    FROM Sale
    WHERE id = ?
  """, (sale_id,))

  row = cursor.fetchone()
  return row

#-------------------------------------
# Lista de ventas
#-------------------------------------
def get_sales(conn):
  cursor = conn.cursor()
  cursor.execute("""
    SELECT
      id,
      sold_at,
      total_amount
    FROM Sale
    ORDER BY sold_at DESC
  """)
  rows = cursor.fetchall()
  return rows
