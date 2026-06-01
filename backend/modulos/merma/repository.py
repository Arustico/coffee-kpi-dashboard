"""
REPOSITORY LAYER - Waste Logging
Solo acceso a datos SQL, sin lógica de transacciones
"""

from typing import Optional

#-------------------------------------------
# REPOSITORY MERMA (WasteLog)
#-------------------------------------------

def create_waste_log(
  conn,
  ingredient_id: int,
  employee_id: int,
  turn_id: int,
  quantity: float,
  reason: Optional[str] = None
) -> int:
  """Inserta un registro de merma"""
  cursor = conn.execute("""
    INSERT INTO WasteLog (ingredient_id, employee_id, turn_id, logged_at, quantity, reason)
    VALUES (?, ?, ?, datetime('now'), ?, ?)
  """, (ingredient_id, employee_id, turn_id, quantity, reason))
  return cursor.lastrowid


def get_waste_log_by_id(conn, waste_id: int):
  """Obtiene un registro de merma por ID"""
  row = conn.execute("""
    SELECT id, ingredient_id, employee_id, turn_id, logged_at, quantity, reason
    FROM WasteLog
    WHERE id = ?
  """, (waste_id,)).fetchone()
  return row


def get_all_waste_logs(conn):
  """Obtiene lista de todos los registros de merma"""
  rows = conn.execute("""
    SELECT id, ingredient_id, employee_id, turn_id, logged_at, quantity, reason
    FROM WasteLog
    ORDER BY logged_at DESC
  """).fetchall()
  return rows


def get_waste_logs_by_ingredient(conn, ingredient_id: int):
  """Obtiene registros de merma de un ingrediente específico"""
  rows = conn.execute("""
    SELECT id, ingredient_id, employee_id, turn_id, logged_at, quantity, reason
    FROM WasteLog
    WHERE ingredient_id = ?
    ORDER BY logged_at DESC
  """, (ingredient_id,)).fetchall()
  return rows


def get_waste_logs_by_employee(conn, employee_id: int):
  """Obtiene registros de merma de un empleado específico"""
  rows = conn.execute("""
    SELECT id, ingredient_id, employee_id, turn_id, logged_at, quantity, reason
    FROM WasteLog
    WHERE employee_id = ?
    ORDER BY logged_at DESC
  """, (employee_id,)).fetchall()
  return rows


def get_waste_logs_by_turn(conn, turn_id: int):
  """Obtiene registros de merma de un turno específico"""
  rows = conn.execute("""
    SELECT id, ingredient_id, employee_id, turn_id, logged_at, quantity, reason
    FROM WasteLog
    WHERE turn_id = ?
    ORDER BY logged_at DESC
  """, (turn_id,)).fetchall()
  return rows


def get_waste_logs_by_date_range(conn, start_date: str, end_date: str):
  """Obtiene registros de merma en un rango de fechas"""
  rows = conn.execute("""
    SELECT id, ingredient_id, employee_id, turn_id, logged_at, quantity, reason
    FROM WasteLog
    WHERE DATE(logged_at) BETWEEN ? AND ?
    ORDER BY logged_at DESC
  """, (start_date, end_date)).fetchall()
  return rows


def delete_waste_log(conn, waste_id: int):
  """Elimina un registro de merma"""
  conn.execute("""
    DELETE FROM WasteLog WHERE id = ?
  """, (waste_id,))


def get_total_waste_by_ingredient(conn, ingredient_id: int) -> float:
  """Calcula la cantidad total de merma de un ingrediente"""
  row = conn.execute("""
    SELECT SUM(quantity) AS total_waste
    FROM WasteLog
    WHERE ingredient_id = ?
  """, (ingredient_id,)).fetchone()

  if row is None or row["total_waste"] is None:
    return 0.0
  return row["total_waste"]


def get_total_waste_by_date_range(conn, start_date: str, end_date: str) -> float:
  """Calcula la cantidad total de merma en un rango de fechas"""
  row = conn.execute("""
    SELECT SUM(quantity) AS total_waste
    FROM WasteLog
    WHERE DATE(logged_at) BETWEEN ? AND ?
  """, (start_date, end_date)).fetchone()

  if row is None or row["total_waste"] is None:
    return 0.0
  return row["total_waste"]


def get_waste_cost_by_ingredient(conn, ingredient_id: int) -> float:
  """
  Calcula el costo total de merma de un ingrediente
  basado en el costo promedio de compras
  """
  row = conn.execute("""
    SELECT SUM(w.quantity * aic.avg_cost) AS total_waste_cost
    FROM WasteLog w
    LEFT JOIN (
      SELECT ingredient_id, SUM(quantity * unit_cost) / SUM(quantity) AS avg_cost
      FROM IngredientPurchase
      GROUP BY ingredient_id
    ) aic ON w.ingredient_id = aic.ingredient_id
    WHERE w.ingredient_id = ?
  """, (ingredient_id,)).fetchone()

  if row is None or row["total_waste_cost"] is None:
    return 0.0

  return row["total_waste_cost"]


def get_total_waste_cost(conn) -> float:
  """Calcula el costo total de toda la merma"""
  row = conn.execute("""
    SELECT SUM(w.quantity * aic.avg_cost) AS total_waste_cost
    FROM WasteLog w
    LEFT JOIN (
      SELECT ingredient_id, SUM(quantity * unit_cost) / SUM(quantity) AS avg_cost
      FROM IngredientPurchase
      GROUP BY ingredient_id
    ) aic ON w.ingredient_id = aic.ingredient_id
  """).fetchone()

  if row is None or row["total_waste_cost"] is None:
    return 0.0
  return row["total_waste_cost"]


def get_waste_ratio_by_date_range(conn, start_date: str, end_date: str) -> dict:
  """
  Calcula el waste ratio (porcentaje de desperdicio)
  en un rango de fechas
  """
  row = conn.execute("""
    SELECT
      SUM(w.quantity * aic.avg_cost) AS total_waste_cost,
      SUM(ic.total_used * aic.avg_cost) AS total_consumption_cost
    FROM WasteLog w
    LEFT JOIN (
      SELECT ingredient_id, SUM(quantity * unit_cost) / SUM(quantity) AS avg_cost
      FROM IngredientPurchase
      GROUP BY ingredient_id
    ) aic ON w.ingredient_id = aic.ingredient_id
    LEFT JOIN (
      SELECT pi.ingredient_id, SUM(si.quantity * pi.quantity) AS total_used
      FROM SaleItem si
      JOIN ProductIngredient pi ON si.product_id = pi.product_id
      GROUP BY pi.ingredient_id
    ) ic ON w.ingredient_id = ic.ingredient_id
    WHERE DATE(w.logged_at) BETWEEN ? AND ?
  """, (start_date, end_date)).fetchone()

  waste_cost = row["total_waste_cost"] or 0.0
  consumption_cost = row["total_consumption_cost"] or 0.0

  total_cost = waste_cost + consumption_cost
  waste_ratio = (waste_cost / total_cost * 100) if total_cost > 0 else 0.0

  return {
    "waste_cost": waste_cost,
    "consumption_cost": consumption_cost,
    "total_cost": total_cost,
    "waste_ratio": waste_ratio
  }


def get_waste_reasons_summary(conn) -> dict:
  """Obtiene resumen de merma por motivo"""
  rows = conn.execute("""
    SELECT reason, COUNT(*) AS count, SUM(quantity) AS total_quantity
    FROM WasteLog
    WHERE reason IS NOT NULL
    GROUP BY reason
    ORDER BY total_quantity DESC
  """).fetchall()

  return [
    {
      "reason": row["reason"],
      "count": row["count"],
      "total_quantity": row["total_quantity"]
    }
    for row in rows
  ]
