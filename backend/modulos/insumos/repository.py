"""
REPOSITORY LAYER - Ingredient Purchases
Solo acceso a datos SQL, sin lógica de transacciones
"""

from typing import Optional

#-------------------------------------------
# REPOSITORY INSUMOS
#-------------------------------------------_

# ==========================================
# INGREDIENT REPOSITORY
# ==========================================

def get_ingredient_by_id(conn, ingredient_id: int):
  """Obtiene un ingrediente por ID"""
  row = conn.execute("""
    SELECT id, name, unit, active
    FROM Ingredient
    WHERE id = ?
  """, (ingredient_id,)).fetchone()

  return row


def get_all_ingredients(conn):
  """Obtiene lista de todos los ingredientes activos"""
  rows = conn.execute("""
    SELECT id, name, unit, active
    FROM Ingredient
    WHERE active = 1
    ORDER BY name
  """).fetchall()

  return rows


def ingredient_exists(conn, ingredient_id: int) -> bool:
  """Verifica si un ingrediente existe"""
  row = conn.execute("""
    SELECT id FROM Ingredient WHERE id = ?
  """, (ingredient_id,)).fetchone()

  return row is not None


def ingredient_is_active(conn, ingredient_id: int) -> bool:
  """Verifica si un ingrediente está activo"""
  row = conn.execute("""
    SELECT active FROM Ingredient WHERE id = ?
  """, (ingredient_id,)).fetchone()

  if row is None:
    return False

  return bool(row["active"])


# ==========================================
# INGREDIENT UNIT REPOSITORY
# ==========================================

def get_ingredient_unit(conn, unit: str):
  """Obtiene una unidad de medida"""
  row = conn.execute("""
    SELECT unit, description
    FROM IngredientUnit
    WHERE unit = ?
  """, (unit,)).fetchone()

  return row


def get_all_ingredient_units(conn):
  """Obtiene lista de todas las unidades de medida"""
  rows = conn.execute("""
    SELECT unit, description
    FROM IngredientUnit
    ORDER BY unit
  """).fetchall()

  return rows


def ingredient_unit_exists(conn, unit: str) -> bool:
  """Verifica si una unidad de medida existe"""
  row = conn.execute("""
    SELECT unit FROM IngredientUnit WHERE unit = ?
  """, (unit,)).fetchone()

  return row is not None


# ==========================================
# SUPPLIER REPOSITORY
# ==========================================

def create_supplier(conn, name: str) -> int:
  """Inserta un nuevo proveedor"""
  cursor = conn.execute("""
    INSERT INTO Supplier (name)
    VALUES (?)
  """, (name,))

  return cursor.lastrowid


def get_supplier_by_id(conn, supplier_id: int):
  """Obtiene un proveedor por ID"""
  row = conn.execute("""
    SELECT id, name
    FROM Supplier
    WHERE id = ?
  """, (supplier_id,)).fetchone()

  return row


def get_all_suppliers(conn):
  """Obtiene lista de todos los proveedores"""
  rows = conn.execute("""
    SELECT id, name
    FROM Supplier
    ORDER BY name
  """).fetchall()

  return rows


def supplier_exists(conn, supplier_id: int) -> bool:
  """Verifica si un proveedor existe"""
  row = conn.execute("""
    SELECT id FROM Supplier WHERE id = ?
  """, (supplier_id,)).fetchone()

  return row is not None


def get_supplier_by_name(conn, name: str):
  """Obtiene un proveedor por nombre"""
  row = conn.execute("""
    SELECT id, name
    FROM Supplier
    WHERE name = ?
  """, (name,)).fetchone()

  return row


def supplier_name_exists(conn, name: str) -> bool:
  """Verifica si un nombre de proveedor ya existe"""
  row = conn.execute("""
    SELECT id FROM Supplier WHERE name = ?
  """, (name,)).fetchone()

  return row is not None


# ==========================================
# INGREDIENT PURCHASE REPOSITORY
# ==========================================

def create_ingredient_purchase(
  conn,
  ingredient_id: int,
  quantity: float,
  unit_cost: float,
  supplier_id: Optional[int] = None
) -> int:
  """Inserta una compra de ingrediente"""
  cursor = conn.execute("""
    INSERT INTO IngredientPurchase (ingredient_id, supplier_id, quantity, unit_cost, purchased_at)
    VALUES (?, ?, ?, ?, datetime('now'))
  """, (ingredient_id, supplier_id, quantity, unit_cost))

  return cursor.lastrowid


def get_purchase_by_id(conn, purchase_id: int):
  """Obtiene una compra por ID"""
  row = conn.execute("""
    SELECT id, ingredient_id, supplier_id, quantity, unit_cost, purchased_at
    FROM IngredientPurchase
    WHERE id = ?
  """, (purchase_id,)).fetchone()

  return row


def get_all_purchases(conn):
  """Obtiene lista de todas las compras"""
  rows = conn.execute("""
    SELECT id, ingredient_id, supplier_id, quantity, unit_cost, purchased_at
    FROM IngredientPurchase
    ORDER BY purchased_at DESC
  """).fetchall()

  return rows


def get_purchases_by_ingredient(conn, ingredient_id: int):
  """Obtiene compras de un ingrediente específico"""
  rows = conn.execute("""
    SELECT id, ingredient_id, supplier_id, quantity, unit_cost, purchased_at
    FROM IngredientPurchase
    WHERE ingredient_id = ?
    ORDER BY purchased_at DESC
  """, (ingredient_id,)).fetchall()

  return rows


def get_purchases_by_supplier(conn, supplier_id: int):
  """Obtiene compras de un proveedor específico"""
  rows = conn.execute("""
    SELECT id, ingredient_id, supplier_id, quantity, unit_cost, purchased_at
    FROM IngredientPurchase
    WHERE supplier_id = ?
    ORDER BY purchased_at DESC
  """, (supplier_id,)).fetchall()

  return rows


def get_purchases_by_date_range(conn, start_date: str, end_date: str):
  """Obtiene compras en un rango de fechas"""
  rows = conn.execute("""
    SELECT id, ingredient_id, supplier_id, quantity, unit_cost, purchased_at
    FROM IngredientPurchase
    WHERE DATE(purchased_at) BETWEEN ? AND ?
    ORDER BY purchased_at DESC
  """, (start_date, end_date)).fetchall()

  return rows


def delete_purchase(conn, purchase_id: int):
  """Elimina una compra"""
  conn.execute("""
    DELETE FROM IngredientPurchase WHERE id = ?
  """, (purchase_id,))


def get_total_purchase_amount(conn, purchase_id: int) -> float:
  """Calcula el monto total de una compra"""
  row = conn.execute("""
    SELECT (quantity * unit_cost) AS total
    FROM IngredientPurchase
    WHERE id = ?
  """, (purchase_id,)).fetchone()

  if row is None:
    return 0.0

  return row["total"]


def get_ingredient_stock_cost(conn, ingredient_id: int) -> dict:
  """
  Obtiene el costo promedio y cantidad total de un ingrediente
  basado en compras históricas
  """
  row = conn.execute("""
    SELECT
      SUM(quantity) AS total_quantity,
      SUM(quantity * unit_cost) / SUM(quantity) AS avg_cost
    FROM IngredientPurchase
    WHERE ingredient_id = ?
  """, (ingredient_id,)).fetchone()

  if row is None or row["total_quantity"] is None:
    return {"total_quantity": 0.0, "avg_cost": 0.0}

  return {
    "total_quantity": row["total_quantity"],
    "avg_cost": row["avg_cost"] or 0.0
  }
