# Lógica del servicio
# - service.py controla la transacción
# - repository.py SOLO ejecuta SQL

from shared.database import get_connection

from .repository import ( # funciones para insertar en bd
  insert_sale,
  insert_sale_item,
  get_product_price
)

def create_sale(data):
  # Inicia conexión
  conn = get_connection()

  try:
    conn.execute("BEGIN") # explicitamos inicio de conexión
    total_amount = 0
    # calculo total de precio
    for item in data.items:
      price = get_product_price(conn, item.product_id)
      total_amount += price * item.quantity


    # Creación de venta
    sale_id = insert_sale(
      conn,
      data.employee_id,
      data.turn_id,
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
  except:Exception as e:
    # deshacer TODO
    conn.rollback()
    raise e
  finally:
    conn.close()

