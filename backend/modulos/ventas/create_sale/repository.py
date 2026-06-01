"""
Definición de funciones para insertar en la base de datos.
  - Solo ejecuta SQL por lo que recibirá la conn (conexión fastAPI)

"""
#-----------------------------------
# Librerias
#-----------------------------------

from fastapi import HTTPException

from datetime import datetime


#-----------------------------------
# Funcion para validación existencia de empleado
#-----------------------------------

def get_current_turn(conn):
  """
  Obtiene el turno automáticamente a partir de la hora de conexión.
  """
  # obtención del momento de la conexión
  current_time = datetime.now().strftime("%H:%M:%S")
  row = conn.execute("""
    SELECT
        id,
        label,
        active
    FROM Turn
    WHERE active = 1
    AND start_time <= ?
    AND end_time >= ?
  """, (
    current_time,
    current_time
  )).fetchone()

  return row

def get_turn_by_id(conn, turn_id: int) -> dict:
  """
  Obtiene el turno acorde al turno_id ingresado manualmente
  """
  row = conn.execute("""
    SELECT
      id,
      label,
      active
    FROM Turn
    WHERE id = ?
  """, (turn_id,)).fetchone()
  return row

#-----------------------------------
# Funcion identificación del turno
#-----------------------------------
def employee_is_active(conn, employee_id: int) -> bool:
  row = conn.execute("""
    SELECT active
    FROM Employee
    WHERE id = ?
  """, (employee_id,)).fetchone()

  if row is None:
    return None

  return bool(row["active"])

#-----------------------------------
# Inserción de una venta
#-----------------------------------

def insert_sale(conn, employee_id: int,
                turn_id: int, total_amount: float) -> int:
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

#-----------------------------------
# Inserción de item
#-----------------------------------
def insert_sale_item(conn, sale_id: int, product_id: int,
                     quantity: int, unit_price: float) -> None:
  """
  Inserta el item vendido en la base de datos
  """
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

#-----------------------------------
# Obtención de precio del producto
#-----------------------------------
def get_product_price(conn, product_id: int) -> float:

  row = conn.execute("""
    SELECT base_price
    FROM Product
    WHERE id = ?
  """, (product_id,)).fetchone()

  if row is None:
    raise HTTPException(
      status_code=404,
      detail=f"Producto {product_id} no existe"
    )

  return row["base_price"]


