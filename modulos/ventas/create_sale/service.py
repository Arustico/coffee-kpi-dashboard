# Lógica del servicio
# - service.py controla la transacción
# - repository.py SOLO ejecuta SQL

# Para el manejo de errores
# ─────────────────────────────────────────────
# LIBRERIAS
# ─────────────────────────────────────────────
from fastapi import HTTPException

from shared.database import get_connection

from .repository import ( # funciones para insertar en bd
  employee_is_active,
  insert_sale,
  insert_sale_item,
  get_product_price,
  get_turn_by_id,
  get_current_turn
)
# ─────────────────────────────────────────────
# Funciones
# ─────────────────────────────────────────────

#-----------------------------------
# Identificación del turno
#-----------------------------------
def resolve_turn(conn, data):
  # Modo admin/manual
  if data.turn_id is not None:
    turn = get_turn_by_id(
      conn,
      data.turn_id)

    if turn is None:
      raise HTTPException(
        status_code=404,
        detail="No existe turno en este horario")

    if not turn["active"]:
      raise HTTPException(
        status_code=400,
        detail="Turno inactivo")
  # Modo automático
  else:
    turn = get_current_turn(conn)
    if turn is None:
      raise HTTPException(
        status_code=400,
        detail="No existe turno activo en este horario")
  return turn

#-----------------------------------
# creación de venta
#-----------------------------------
def create_sale(data):
  # Inicia conexión
  conn = get_connection()

  try:
    conn.execute("BEGIN") # explicitamos inicio de conexión

    # Validación del turno
    turno = resolve_turn(conn, data)
    turn_id = turno["id"]

    # Validación del empleado
    employee_status = employee_is_active(conn, data.employee_id)

    if employee_status is None:
      raise HTTPException(
        status_code=404,
        detail="Empleado no existe")

    if not employee_status:
      raise HTTPException(
        status_code=400,
        detail="Empleado inactivo")

    # calculo total de precio
    total_amount = 0
    for item in data.items:
      price = get_product_price(conn, item.product_id)
      total_amount += price * item.quantity

    # Creación de venta
    sale_id = insert_sale(
      conn,
      data.employee_id,
      turn_id,
      total_amount
    )

    # crear items
    for item in data.items:
      price = get_product_price(conn, item.product_id)
      insert_sale_item(
        conn,
        sale_id,
        item.product_id,
        item.quantity,
        price
      )
    # SI todo OK entonces enviamos commit
    conn.commit()
    # retornamos
    return {
      "sale_id": sale_id,
      "total_amount": total_amount}
  except HTTPException:
    conn.rollback()
    raise

  except Exception as e:
    # deshacer todo
    conn.rollback()
    raise HTTPException(
      status_code=500,
      detail=f"Error interno al crear venta {e}"
    )

  finally:
    conn.close()


