"""
API LAYER - KPIs and Reports
Rutas HTTP
"""

from fastapi import APIRouter, Depends, Query
from shared.security.dependencies import get_current_user
from modulos.KPIs.schemas import (
  RevenueResponse, ProductRevenueListResponse,
  CogsResponse, GrossProfitResponse, ProductMarginListResponse,
  WasteRatioResponse, DailySalesResponse, TurnSalesResponse, EmployeeSalesResponse,
  DashboardMetricsResponse, DateRangeRequest
)
from modulos.KPIs.service import (
  get_total_revenue_service, get_revenue_by_date_range_service,
  get_all_products_revenue_service, get_top_products_service,
  get_gross_profit_service, get_cogs_service, get_product_margins_service,
  get_waste_ratio_service, get_waste_ratio_by_date_range_service,
  get_daily_sales_service, get_turn_sales_service, get_employee_sales_service,
  get_dashboard_metrics_service
)

router = APIRouter(prefix="/kpis", tags=["kpis"])


# ==========================================
# DASHBOARD MAIN
# ==========================================

@router.get(
  "/dashboard",
  response_model=DashboardMetricsResponse,
  summary="Dashboard principal",
  description="Obtiene todas las métricas principales"
)
def get_dashboard_metrics(current_user = Depends(get_current_user)):
  """Obtiene las métricas principales del dashboard"""
  return get_dashboard_metrics_service()


# ==========================================
# REVENUE
# ==========================================

@router.get(
  "/revenue/total",
  response_model=RevenueResponse,
  summary="Ingreso total",
  description="Obtiene el ingreso total acumulado"
)
def get_total_revenue(current_user = Depends(get_current_user)):
  """Obtiene el ingreso total"""
  return get_total_revenue_service()


@router.post(
  "/revenue/by-date-range",
  response_model=RevenueResponse,
  summary="Ingreso por rango de fechas",
  description="Obtiene ingreso en un rango de fechas"
)
def get_revenue_by_date_range(
  data: DateRangeRequest,
  current_user = Depends(get_current_user)
):
  """
  Obtiene ingreso en un rango de fechas

  - **start_date**: Fecha inicio (YYYY-MM-DD)
  - **end_date**: Fecha fin (YYYY-MM-DD)
  """
  return get_revenue_by_date_range_service(data)


@router.get(
  "/revenue/products",
  response_model=ProductRevenueListResponse,
  summary="Revenue por producto",
  description="Obtiene revenue de todos los productos"
)
def get_products_revenue(current_user = Depends(get_current_user)):
  """Obtiene revenue de todos los productos"""
  return get_all_products_revenue_service()


@router.get(
  "/revenue/top-products",
  response_model=ProductRevenueListResponse,
  summary="Top productos",
  description="Obtiene los productos con mayor revenue"
)
def get_top_products(
  limit: int = Query(10, ge=1, le=100),
  current_user = Depends(get_current_user)
):
  """Obtiene los productos con mayor revenue"""
  return get_top_products_service(limit)


# ==========================================
# COST & MARGIN
# ==========================================

@router.get(
  "/cogs",
  response_model=CogsResponse,
  summary="Costo de bienes vendidos",
  description="Obtiene el COGS total"
)
def get_cogs(current_user = Depends(get_current_user)):
  """Obtiene el costo total de bienes vendidos"""
  return get_cogs_service()


@router.get(
  "/gross-profit",
  response_model=GrossProfitResponse,
  summary="Ganancia bruta",
  description="Obtiene la ganancia bruta y margen"
)
def get_gross_profit(current_user = Depends(get_current_user)):
  """Obtiene la ganancia bruta y margen bruto"""
  return get_gross_profit_service()


@router.get(
  "/margins/products",
  response_model=ProductMarginListResponse,
  summary="Márgenes por producto",
  description="Obtiene márgenes de todos los productos"
)
def get_product_margins(current_user = Depends(get_current_user)):
  """Obtiene los márgenes de todos los productos"""
  return get_product_margins_service()


# ==========================================
# WASTE
# ==========================================

@router.get(
  "/waste-ratio",
  response_model=WasteRatioResponse,
  summary="Ratio de desperdicio",
  description="Obtiene el waste ratio total"
)
def get_waste_ratio(current_user = Depends(get_current_user)):
  """Obtiene el ratio de desperdicio"""
  return get_waste_ratio_service()


@router.post(
  "/waste-ratio/by-date-range",
  response_model=WasteRatioResponse,
  summary="Waste ratio por rango de fechas",
  description="Obtiene waste ratio en un rango de fechas"
)
def get_waste_ratio_by_date_range(
  data: DateRangeRequest,
  current_user = Depends(get_current_user)
):
  """
  Obtiene waste ratio en un rango de fechas

  - **start_date**: Fecha inicio (YYYY-MM-DD)
  - **end_date**: Fecha fin (YYYY-MM-DD)
  """
  return get_waste_ratio_by_date_range_service(data)


# ==========================================
# SALES SUMMARY
# ==========================================

@router.get(
  "/sales/daily/{date}",
  response_model=DailySalesResponse,
  summary="Ventas del día",
  description="Obtiene resumen de ventas de un día específico"
)
def get_daily_sales(
  date: str,
  current_user = Depends(get_current_user)
):
  """
  Obtiene resumen de ventas de un día

  - **date**: Fecha (YYYY-MM-DD)
  """
  return get_daily_sales_service(date)


@router.get(
  "/sales/by-turn/{turn_id}",
  response_model=TurnSalesResponse,
  summary="Ventas por turno",
  description="Obtiene resumen de ventas de un turno"
)
def get_turn_sales(
  turn_id: int,
  current_user = Depends(get_current_user)
):
  """Obtiene resumen de ventas de un turno específico"""
  return get_turn_sales_service(turn_id)


@router.get(
  "/sales/by-employee/{employee_id}",
  response_model=EmployeeSalesResponse,
  summary="Ventas por empleado",
  description="Obtiene resumen de ventas de un empleado"
)
def get_employee_sales(
  employee_id: int,
  current_user = Depends(get_current_user)
):
  """Obtiene resumen de ventas de un empleado específico"""
  return get_employee_sales_service(employee_id)
