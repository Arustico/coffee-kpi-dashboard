"""
REPOSITORY LAYER - KPIs and Reports
Solo acceso a datos SQL, sin lógica de transacciones
"""

from typing import Optional

# ==========================================
# REPOSITORY KPIs
# ==========================================

# ==========================================
# REVENUE KPIs
# ==========================================

def get_total_revenue(conn) -> float:
  """Calcula el ingreso total de todas las ventas"""
  row = conn.execute("""
    SELECT SUM(total_amount) AS total_revenue
    FROM Sale
  """).fetchone()

  if row is None or row["total_revenue"] is None:
    return 0.0

  return row["total_revenue"]


def get_revenue_by_date_range(conn, start_date: str, end_date: str) -> float:
  """Calcula ingreso en un rango de fechas"""
  row = conn.execute("""
    SELECT SUM(total_amount) AS total_revenue
    FROM Sale
    WHERE DATE(sold_at) BETWEEN ? AND ?
  """, (start_date, end_date)).fetchone()

  if row is None or row["total_revenue"] is None:
    return 0.0

  return row["total_revenue"]


def get_revenue_by_turn(conn, turn_id: int) -> float:
  """Calcula ingreso por turno"""
  row = conn.execute("""
    SELECT SUM(total_amount) AS total_revenue
    FROM Sale
    WHERE turn_id = ?
  """, (turn_id,)).fetchone()

  if row is None or row["total_revenue"] is None:
    return 0.0

  return row["total_revenue"]


def get_revenue_by_employee(conn, employee_id: int) -> float:
  """Calcula ingreso por empleado"""
  row = conn.execute("""
    SELECT SUM(total_amount) AS total_revenue
    FROM Sale
    WHERE employee_id = ?
  """, (employee_id,)).fetchone()

  if row is None or row["total_revenue"] is None:
    return 0.0

  return row["total_revenue"]


def get_daily_revenue(conn, date: str) -> float:
  """Calcula ingreso del día"""
  row = conn.execute("""
    SELECT SUM(total_amount) AS total_revenue
    FROM Sale
    WHERE DATE(sold_at) = ?
  """, (date,)).fetchone()

  if row is None or row["total_revenue"] is None:
    return 0.0

  return row["total_revenue"]


# ==========================================
# PRODUCT KPIs
# ==========================================

def get_product_revenue(conn, product_id: int) -> dict:
  """Obtiene revenue de un producto específico"""
  row = conn.execute("""
    SELECT
      p.id,
      p.name,
      p.base_price,
      SUM(si.quantity) AS total_units,
      SUM(si.quantity * si.unit_price) AS total_revenue
    FROM Product p
    LEFT JOIN SaleItem si ON p.id = si.product_id
    WHERE p.id = ?
    GROUP BY p.id
  """, (product_id,)).fetchone()

  if row is None:
    return {
      "product_id": product_id,
      "total_units": 0,
      "total_revenue": 0.0
    }

  return {
    "product_id": row["id"],
    "product_name": row["name"],
    "base_price": row["base_price"],
    "total_units": row["total_units"] or 0,
    "total_revenue": row["total_revenue"] or 0.0
  }


def get_all_products_revenue(conn) -> list:
  """Obtiene revenue de todos los productos"""
  rows = conn.execute("""
    SELECT
      p.id,
      p.name,
      p.base_price,
      SUM(si.quantity) AS total_units,
      SUM(si.quantity * si.unit_price) AS total_revenue
    FROM Product p
    LEFT JOIN SaleItem si ON p.id = si.product_id
    WHERE p.active = 1
    GROUP BY p.id
    ORDER BY total_revenue DESC
  """).fetchall()

  return [
    {
      "product_id": row["id"],
      "product_name": row["name"],
      "base_price": row["base_price"],
      "total_units": row["total_units"] or 0,
      "total_revenue": row["total_revenue"] or 0.0
    }
    for row in rows
  ]


def get_top_products(conn, limit: int = 10) -> list:
  """Obtiene los productos con mayor revenue"""
  rows = conn.execute("""
    SELECT
      p.id,
      p.name,
      SUM(si.quantity) AS total_units,
      SUM(si.quantity * si.unit_price) AS total_revenue
    FROM Product p
    JOIN SaleItem si ON p.id = si.product_id
    GROUP BY p.id
    ORDER BY total_revenue DESC
    LIMIT ?
  """, (limit,)).fetchall()

  return [
    {
      "product_id": row["id"],
      "product_name": row["name"],
      "total_units": row["total_units"],
      "total_revenue": row["total_revenue"]
    }
    for row in rows
  ]


# ==========================================
# COST OF GOODS SOLD (COGS)
# ==========================================

def get_product_cost(conn, product_id: int) -> float:
  """Calcula el costo teórico de un producto"""
  row = conn.execute("""
    SELECT SUM(pi.quantity * aic.avg_cost) AS cost_per_unit
    FROM ProductIngredient pi
    LEFT JOIN (
      SELECT ingredient_id, SUM(quantity * unit_cost) / SUM(quantity) AS avg_cost
      FROM IngredientPurchase
      GROUP BY ingredient_id
    ) aic ON pi.ingredient_id = aic.ingredient_id
    WHERE pi.product_id = ?
  """, (product_id,)).fetchone()

  if row is None or row["cost_per_unit"] is None:
    return 0.0

  return row["cost_per_unit"]


def get_total_cogs(conn) -> float:
  """Calcula el costo total de bienes vendidos"""
  row = conn.execute("""
    SELECT
      SUM(si.quantity * pc.cost_per_unit) AS total_cogs
    FROM SaleItem si
    JOIN (
      SELECT
        p.id,
        SUM(pi.quantity * aic.avg_cost) AS cost_per_unit
      FROM Product p
      LEFT JOIN ProductIngredient pi ON p.id = pi.product_id
      LEFT JOIN (
        SELECT ingredient_id, SUM(quantity * unit_cost) / SUM(quantity) AS avg_cost
        FROM IngredientPurchase
        GROUP BY ingredient_id
      ) aic ON pi.ingredient_id = aic.ingredient_id
      GROUP BY p.id
    ) pc ON si.product_id = pc.id
  """).fetchone()

  if row is None or row["total_cogs"] is None:
    return 0.0

  return row["total_cogs"]


# ==========================================
# MARGIN & PROFIT
# ==========================================

def get_gross_profit(conn) -> float:
  """Calcula la ganancia bruta"""
  row = conn.execute("""
    SELECT
      SUM(s.total_amount) - SUM(si.quantity * pc.cost_per_unit) AS gross_profit
    FROM Sale s
    JOIN SaleItem si ON s.id = si.sale_id
    JOIN (
      SELECT
        p.id,
        SUM(pi.quantity * aic.avg_cost) AS cost_per_unit
      FROM Product p
      LEFT JOIN ProductIngredient pi ON p.id = pi.product_id
      LEFT JOIN (
        SELECT ingredient_id, SUM(quantity * unit_cost) / SUM(quantity) AS avg_cost
        FROM IngredientPurchase
        GROUP BY ingredient_id
      ) aic ON pi.ingredient_id = aic.ingredient_id
      GROUP BY p.id
    ) pc ON si.product_id = pc.id
  """).fetchone()

  if row is None or row["gross_profit"] is None:
    return 0.0

  return row["gross_profit"]


def get_gross_margin_percentage(conn) -> float:
  """Calcula el margen bruto (%)"""
  revenue_row = conn.execute("SELECT SUM(total_amount) AS total_revenue FROM Sale").fetchone()

  if revenue_row is None or revenue_row["total_revenue"] is None or revenue_row["total_revenue"] == 0:
    return 0.0

  total_revenue = revenue_row["total_revenue"]
  gross_profit = get_gross_profit(conn)

  return (gross_profit / total_revenue) * 100


def get_product_margin(conn, product_id: int) -> dict:
  """Calcula el margen de un producto específico"""
  row = conn.execute("""
    SELECT
      si.product_id,
      SUM(si.quantity) AS total_units,
      SUM(si.quantity * si.unit_price) AS revenue,
      SUM(si.quantity * pc.cost_per_unit) AS total_cost,
      SUM(si.quantity * si.unit_price) - SUM(si.quantity * pc.cost_per_unit) AS gross_profit,
      (SUM(si.quantity * si.unit_price) - SUM(si.quantity * pc.cost_per_unit)) * 100.0 / SUM(si.quantity * si.unit_price) AS margin_percentage
    FROM SaleItem si
    JOIN (
      SELECT
        p.id,
        SUM(pi.quantity * aic.avg_cost) AS cost_per_unit
      FROM Product p
      LEFT JOIN ProductIngredient pi ON p.id = pi.product_id
      LEFT JOIN (
        SELECT ingredient_id, SUM(quantity * unit_cost) / SUM(quantity) AS avg_cost
        FROM IngredientPurchase
        GROUP BY ingredient_id
      ) aic ON pi.ingredient_id = aic.ingredient_id
      GROUP BY p.id
    ) pc ON si.product_id = pc.id
    WHERE si.product_id = ?
    GROUP BY si.product_id
  """, (product_id,)).fetchone()

  if row is None:
    return {
      "product_id": product_id,
      "total_units": 0,
      "revenue": 0.0,
      "total_cost": 0.0,
      "gross_profit": 0.0,
      "margin_percentage": 0.0
    }

  return {
    "product_id": row["product_id"],
    "total_units": row["total_units"] or 0,
    "revenue": row["revenue"] or 0.0,
    "total_cost": row["total_cost"] or 0.0,
    "gross_profit": row["gross_profit"] or 0.0,
    "margin_percentage": row["margin_percentage"] or 0.0
  }


# ==========================================
# WASTE RATIO & INVENTORY
# ==========================================

def get_waste_ratio(conn) -> dict:
  """Calcula el waste ratio (porcentaje de desperdicio)"""
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
  """).fetchone()

  waste_cost = row["total_waste_cost"] or 0.0 if row else 0.0
  consumption_cost = row["total_consumption_cost"] or 0.0 if row else 0.0
  total_cost = waste_cost + consumption_cost
  waste_ratio = (waste_cost / total_cost * 100) if total_cost > 0 else 0.0

  return {
    "waste_cost": waste_cost,
    "consumption_cost": consumption_cost,
    "total_cost": total_cost,
    "waste_ratio": waste_ratio
  }


def get_waste_ratio_by_date_range(conn, start_date: str, end_date: str) -> dict:
  """Calcula el waste ratio en un rango de fechas"""
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
      WHERE DATE(si.sale_id) IN (SELECT id FROM Sale WHERE DATE(sold_at) BETWEEN ? AND ?)
      GROUP BY pi.ingredient_id
    ) ic ON w.ingredient_id = ic.ingredient_id
    WHERE DATE(w.logged_at) BETWEEN ? AND ?
  """, (start_date, end_date, start_date, end_date)).fetchone()

  waste_cost = row["total_waste_cost"] or 0.0 if row else 0.0
  consumption_cost = row["total_consumption_cost"] or 0.0 if row else 0.0
  total_cost = waste_cost + consumption_cost
  waste_ratio = (waste_cost / total_cost * 100) if total_cost > 0 else 0.0

  return {
    "waste_cost": waste_cost,
    "consumption_cost": consumption_cost,
    "total_cost": total_cost,
    "waste_ratio": waste_ratio
  }


# ==========================================
# DAILY SALES SUMMARY
# ==========================================

def get_daily_sales_summary(conn, date: str) -> dict:
  """Obtiene resumen de ventas del día"""
  row = conn.execute("""
    SELECT
      DATE(s.sold_at) AS date,
      COUNT(s.id) AS total_sales,
      SUM(s.total_amount) AS total_revenue,
      SUM(si.quantity) AS total_units,
      AVG(s.total_amount) AS avg_sale
    FROM Sale s
    LEFT JOIN SaleItem si ON s.id = si.sale_id
    WHERE DATE(s.sold_at) = ?
    GROUP BY DATE(s.sold_at)
  """, (date,)).fetchone()

  if row is None:
    return {
      "date": date,
      "total_sales": 0,
      "total_revenue": 0.0,
      "total_units": 0,
      "avg_sale": 0.0
    }

  return {
    "date": row["date"],
    "total_sales": row["total_sales"] or 0,
    "total_revenue": row["total_revenue"] or 0.0,
    "total_units": row["total_units"] or 0,
    "avg_sale": row["avg_sale"] or 0.0
  }


def get_sales_by_turn_summary(conn, turn_id: int) -> dict:
  """Obtiene resumen de ventas por turno"""
  row = conn.execute("""
    SELECT
      s.turn_id,
      t.label,
      COUNT(s.id) AS total_sales,
      SUM(s.total_amount) AS total_revenue,
      SUM(si.quantity) AS total_units,
      AVG(s.total_amount) AS avg_sale
    FROM Sale s
    LEFT JOIN SaleItem si ON s.id = si.sale_id
    LEFT JOIN Turn t ON s.turn_id = t.id
    WHERE s.turn_id = ?
    GROUP BY s.turn_id
  """, (turn_id,)).fetchone()

  if row is None:
    return {
      "turn_id": turn_id,
      "turn_label": None,
      "total_sales": 0,
      "total_revenue": 0.0,
      "total_units": 0,
      "avg_sale": 0.0
    }

  return {
    "turn_id": row["turn_id"],
    "turn_label": row["label"],
    "total_sales": row["total_sales"] or 0,
    "total_revenue": row["total_revenue"] or 0.0,
    "total_units": row["total_units"] or 0,
    "avg_sale": row["avg_sale"] or 0.0
  }


def get_sales_by_employee_summary(conn, employee_id: int) -> dict:
  """Obtiene resumen de ventas por empleado"""
  row = conn.execute("""
    SELECT
      s.employee_id,
      e.full_name,
      COUNT(s.id) AS total_sales,
      SUM(s.total_amount) AS total_revenue,
      SUM(si.quantity) AS total_units,
      AVG(s.total_amount) AS avg_sale
    FROM Sale s
    LEFT JOIN SaleItem si ON s.id = si.sale_id
    LEFT JOIN Employee e ON s.employee_id = e.id
    WHERE s.employee_id = ?
    GROUP BY s.employee_id
  """, (employee_id,)).fetchone()

  if row is None:
    return {
      "employee_id": employee_id,
      "employee_name": None,
      "total_sales": 0,
      "total_revenue": 0.0,
      "total_units": 0,
      "avg_sale": 0.0
    }

  return {
    "employee_id": row["employee_id"],
    "employee_name": row["full_name"],
    "total_sales": row["total_sales"] or 0,
    "total_revenue": row["total_revenue"] or 0.0,
    "total_units": row["total_units"] or 0,
    "avg_sale": row["avg_sale"] or 0.0
  }


# ==========================================
# GENERAL DASHBOARD METRICS
# ==========================================

def get_dashboard_metrics(conn) -> dict:
  """Obtiene métricas principales del dashboard"""
  revenue = get_total_revenue(conn)
  cogs = get_total_cogs(conn)
  gross_profit = revenue - cogs
  gross_margin = (gross_profit / revenue * 100) if revenue > 0 else 0.0
  waste_data = get_waste_ratio(conn)

  sales_count = conn.execute("SELECT COUNT(*) AS count FROM Sale").fetchone()
  products_count = conn.execute("SELECT COUNT(*) AS count FROM Product WHERE active = 1").fetchone()

  return {
    "total_revenue": revenue,
    "total_cogs": cogs,
    "gross_profit": gross_profit,
    "gross_margin_percentage": gross_margin,
    "waste_cost": waste_data["waste_cost"],
    "waste_ratio_percentage": waste_data["waste_ratio"],
    "total_sales": sales_count["count"] if sales_count else 0,
    "active_products": products_count["count"] if products_count else 0
  }
