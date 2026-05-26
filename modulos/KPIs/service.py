"""
SERVICE LAYER - KPIs and Reports
Lógica de negocio, validaciones
"""

from fastapi import HTTPException
from shared.database import get_connection
from modulos.kpis.repository import (
  get_total_revenue, get_revenue_by_date_range, get_revenue_by_turn, get_revenue_by_employee,
  get_daily_revenue, get_product_revenue, get_all_products_revenue, get_top_products,
  get_product_cost, get_total_cogs, get_gross_profit, get_gross_margin_percentage,
  get_product_margin, get_waste_ratio, get_waste_ratio_by_date_range,
  get_daily_sales_summary, get_sales_by_turn_summary, get_sales_by_employee_summary,
  get_dashboard_metrics
)
from modulos.kpis.schemas import (
  RevenueResponse, ProductRevenueResponse, ProductRevenueListResponse,
  CogsResponse, GrossProfitResponse, ProductMarginResponse, ProductMarginListResponse,
  WasteRatioResponse, DailySalesResponse, TurnSalesResponse, EmployeeSalesResponse,
  DashboardMetricsResponse, DateRangeRequest
)
import logging

logger = logging.getLogger(__name__)


# ==========================================
# REVENUE SERVICES
# ==========================================

def get_total_revenue_service() -> RevenueResponse:
  """Obtiene ingreso total"""
  conn = get_connection()

  try:
    revenue = get_total_revenue(conn)
    logger.info("Ingreso total obtenido")

    return RevenueResponse(total_revenue=revenue)

  except Exception as e:
    logger.error(f"Error al obtener ingreso total: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener ingreso total"
    )
  finally:
    conn.close()


def get_revenue_by_date_range_service(data: DateRangeRequest) -> RevenueResponse:
  """Obtiene ingreso en un rango de fechas"""
  conn = get_connection()

  try:
    revenue = get_revenue_by_date_range(conn, data.start_date, data.end_date)
    logger.info(f"Ingreso por rango de fechas: {data.start_date} a {data.end_date}")

    return RevenueResponse(total_revenue=revenue)

  except Exception as e:
    logger.error(f"Error al obtener ingreso: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener ingreso"
    )
  finally:
    conn.close()


def get_all_products_revenue_service() -> ProductRevenueListResponse:
  """Obtiene revenue de todos los productos"""
  conn = get_connection()

  try:
    products = get_all_products_revenue(conn)

    products_response = [
      ProductRevenueResponse(
        product_id=p["product_id"],
        product_name=p["product_name"],
        base_price=p["base_price"],
        total_units=p["total_units"],
        total_revenue=p["total_revenue"]
      )
      for p in products
    ]

    logger.info(f"Revenue de productos obtenido: {len(products_response)} productos")

    return ProductRevenueListResponse(
      products=products_response,
      total=len(products_response)
    )

  except Exception as e:
    logger.error(f"Error al obtener revenue: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener revenue de productos"
    )
  finally:
    conn.close()


def get_top_products_service(limit: int = 10) -> ProductRevenueListResponse:
  """Obtiene los productos con mayor revenue"""
  conn = get_connection()

  try:
    if limit < 1 or limit > 100:
      limit = 10

    products = get_top_products(conn, limit)

    products_response = [
      ProductRevenueResponse(
        product_id=p["product_id"],
        product_name=p["product_name"],
        base_price=0.0,
        total_units=p["total_units"],
        total_revenue=p["total_revenue"]
      )
      for p in products
    ]

    logger.info(f"Top {limit} productos obtenido")

    return ProductRevenueListResponse(
      products=products_response,
      total=len(products_response)
    )

  except Exception as e:
    logger.error(f"Error al obtener top productos: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener top productos"
    )
  finally:
    conn.close()


# ==========================================
# COST & MARGIN SERVICES
# ==========================================

def get_gross_profit_service() -> GrossProfitResponse:
  """Obtiene ganancia bruta"""
  conn = get_connection()

  try:
    gross_profit = get_gross_profit(conn)
    margin_percentage = get_gross_margin_percentage(conn)

    logger.info("Ganancia bruta obtenida")

    return GrossProfitResponse(
      gross_profit=gross_profit,
      gross_margin_percentage=margin_percentage
    )

  except Exception as e:
    logger.error(f"Error al obtener ganancia bruta: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener ganancia bruta"
    )
  finally:
    conn.close()


def get_cogs_service() -> CogsResponse:
  """Obtiene costo de bienes vendidos"""
  conn = get_connection()

  try:
    cogs = get_total_cogs(conn)
    logger.info("COGS obtenido")

    return CogsResponse(total_cogs=cogs)

  except Exception as e:
    logger.error(f"Error al obtener COGS: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener COGS"
    )
  finally:
    conn.close()


def get_product_margins_service() -> ProductMarginListResponse:
  """Obtiene márgenes de todos los productos"""
  conn = get_connection()

  try:
    products = get_all_products_revenue(conn)

    margins = []
    for product in products:
      margin_data = get_product_margin(conn, product["product_id"])
      if margin_data["total_units"] > 0:
        margins.append(
          ProductMarginResponse(
            product_id=margin_data["product_id"],
            total_units=margin_data["total_units"],
            revenue=margin_data["revenue"],
            total_cost=margin_data["total_cost"],
            gross_profit=margin_data["gross_profit"],
            margin_percentage=margin_data["margin_percentage"]
          )
        )

    logger.info(f"Márgenes de productos obtenido: {len(margins)} productos")

    return ProductMarginListResponse(
      products=margins,
      total=len(margins)
    )

  except Exception as e:
    logger.error(f"Error al obtener márgenes: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener márgenes de productos"
    )
  finally:
    conn.close()


# ==========================================
# WASTE SERVICES
# ==========================================

def get_waste_ratio_service() -> WasteRatioResponse:
  """Obtiene ratio de desperdicio"""
  conn = get_connection()

  try:
    waste_data = get_waste_ratio(conn)
    logger.info("Waste ratio obtenido")

    return WasteRatioResponse(
      waste_cost=waste_data["waste_cost"],
      consumption_cost=waste_data["consumption_cost"],
      total_cost=waste_data["total_cost"],
      waste_ratio_percentage=waste_data["waste_ratio"]
    )

  except Exception as e:
    logger.error(f"Error al obtener waste ratio: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener waste ratio"
    )
  finally:
    conn.close()


def get_waste_ratio_by_date_range_service(data: DateRangeRequest) -> WasteRatioResponse:
  """Obtiene waste ratio en un rango de fechas"""
  conn = get_connection()

  try:
    waste_data = get_waste_ratio_by_date_range(conn, data.start_date, data.end_date)
    logger.info(f"Waste ratio por rango de fechas: {data.start_date} a {data.end_date}")

    return WasteRatioResponse(
      waste_cost=waste_data["waste_cost"],
      consumption_cost=waste_data["consumption_cost"],
      total_cost=waste_data["total_cost"],
      waste_ratio_percentage=waste_data["waste_ratio"]
    )

  except Exception as e:
    logger.error(f"Error al obtener waste ratio: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener waste ratio"
    )
  finally:
    conn.close()


# ==========================================
# SALES SUMMARY SERVICES
# ==========================================

def get_daily_sales_service(date: str) -> DailySalesResponse:
  """Obtiene resumen de ventas del día"""
  conn = get_connection()

  try:
    summary = get_daily_sales_summary(conn, date)
    logger.info(f"Resumen de ventas del día: {date}")

    return DailySalesResponse(
      date=summary["date"],
      total_sales=summary["total_sales"],
      total_revenue=summary["total_revenue"],
      total_units=summary["total_units"],
      avg_sale=summary["avg_sale"]
    )

  except Exception as e:
    logger.error(f"Error al obtener resumen diario: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener resumen de ventas"
    )
  finally:
    conn.close()


def get_turn_sales_service(turn_id: int) -> TurnSalesResponse:
  """Obtiene resumen de ventas por turno"""
  conn = get_connection()

  try:
    summary = get_sales_by_turn_summary(conn, turn_id)
    logger.info(f"Resumen de ventas por turno: {turn_id}")

    return TurnSalesResponse(
      turn_id=summary["turn_id"],
      turn_label=summary["turn_label"],
      total_sales=summary["total_sales"],
      total_revenue=summary["total_revenue"],
      total_units=summary["total_units"],
      avg_sale=summary["avg_sale"]
    )

  except Exception as e:
    logger.error(f"Error al obtener resumen por turno: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener resumen por turno"
    )
  finally:
    conn.close()


def get_employee_sales_service(employee_id: int) -> EmployeeSalesResponse:
  """Obtiene resumen de ventas por empleado"""
  conn = get_connection()

  try:
    summary = get_sales_by_employee_summary(conn, employee_id)
    logger.info(f"Resumen de ventas por empleado: {employee_id}")

    return EmployeeSalesResponse(
      employee_id=summary["employee_id"],
      employee_name=summary["employee_name"],
      total_sales=summary["total_sales"],
      total_revenue=summary["total_revenue"],
      total_units=summary["total_units"],
      avg_sale=summary["avg_sale"]
    )

  except Exception as e:
    logger.error(f"Error al obtener resumen por empleado: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener resumen por empleado"
    )
  finally:
    conn.close()


# ==========================================
# DASHBOARD MAIN SERVICE
# ==========================================

def get_dashboard_metrics_service() -> DashboardMetricsResponse:
  """Obtiene métricas principales del dashboard"""
  conn = get_connection()

  try:
    metrics = get_dashboard_metrics(conn)
    logger.info("Métricas del dashboard obtenidas")

    return DashboardMetricsResponse(
      total_revenue=metrics["total_revenue"],
      total_cogs=metrics["total_cogs"],
      gross_profit=metrics["gross_profit"],
      gross_margin_percentage=metrics["gross_margin_percentage"],
      waste_cost=metrics["waste_cost"],
      waste_ratio_percentage=metrics["waste_ratio_percentage"],
      total_sales=metrics["total_sales"],
      active_products=metrics["active_products"]
    )

  except Exception as e:
    logger.error(f"Error al obtener métricas del dashboard: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener métricas del dashboard"
    )
  finally:
    conn.close()
