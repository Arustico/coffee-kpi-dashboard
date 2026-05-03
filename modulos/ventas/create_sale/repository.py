"""
Definición de funciones para insertar en la base de datos.
  - Solo ejecuta SQL por lo que recibirá la conn (conexión fastAPI)

"""


# Inserción de una venta
def insert_sale(conn, employee_id, turn_id, total_amount):
  conn = get_connection()

  cursor = conn.execute(
    """
    INSERT INTO Sale (
        employee_id,
        turn_id,
        sold_at,
        total_amount
    )
    VALUES (?, ?, datetime('now'), ?)
    """,
    (employee_id, turn_id, total_amount)
  )

  return cursor.lastrowid


# Insertación de item

def insert_sale_item(conn, sale_id, product_id, quantity, unit_price):
  conn.execute(
    """
      INSERT INTO SaleItem (
          sale_id,
          product_id,
          quantity,
          unit_price
      )
      VALUES (?, ?, ?, ?)
    """,
    (
      sale_id,
      product_id,
      quantity,
      unit_price))


# Obtención de precio del producto

def get_product_price(conn, product_id):

  row = conn.execute("""
    SELECT base_price
    FROM Product
    WHERE id = ?
  """, (product_id,)).fetchone()

  return row["base_price"]


