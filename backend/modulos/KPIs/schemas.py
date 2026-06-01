from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ==========================================
# SCHEMAS KPIs
# ==========================================

# ==========================================
# REQUESTS
# ==========================================

class DateRangeRequest(BaseModel):
  """Filtro de rango de fechas"""
  start_date: str = Field(description="Fecha inicio (YYYY-MM-DD)")
  end_date: str = Field(description="Fecha fin (YYYY-MM-DD)")

  class Config:
    json_schema_extra = {
      "example": {
        "start_date": "2026-05-01",
        "end_date": "2026-05-31"
      }
    }


# ==========================================
# RESPONSES - REVENUE
# ==========================================

class RevenueResponse(BaseModel):
  """Respuesta de ingresos"""
  total_revenue: float = Field(description="Ingreso total en pesos")

  class Config:
    json_schema_extra = {
      "example": {
        "total_revenue": 125000.00
      }
    }


class ProductRevenueResponse(BaseModel):
  """Revenue de un producto"""
  product_id: int
  product_name: str
  base_price: float
  total_units: int
  total_revenue: float

  class Config:
    json_schema_extra = {
      "example": {
        "product_id": 1,
        "product_name": "Latte",
        "base_price": 3000.0,
        "total_units": 42,
        "total_revenue": 126000.0
      }
    }


class ProductRevenueListResponse(BaseModel):
  """Lista de revenue por producto"""
  products: List[ProductRevenueResponse]
  total: int

  class Config:
    json_schema_extra = {
      "example": {
        "products": [],
        "total": 0
      }
    }


# ==========================================
# RESPONSES - COST & MARGIN
# ==========================================

class CogsResponse(BaseModel):
  """Costo de bienes vendidos"""
  total_cogs: float = Field(description="Costo total de bienes vendidos")

  class Config:
    json_schema_extra = {
      "example": {
        "total_cogs": 45000.00
      }
    }


class GrossProfitResponse(BaseModel):
  """Ganancia bruta"""
  gross_profit: float = Field(description="Ganancia bruta")
  gross_margin_percentage: float = Field(description="Margen bruto (%)")

  class Config:
    json_schema_extra = {
      "example": {
        "gross_profit": 80000.00,
        "gross_margin_percentage": 64.0
      }
    }


class ProductMarginResponse(BaseModel):
  """Margen de un producto"""
  product_id: int
  total_units: int
  revenue: float
  total_cost: float
  gross_profit: float
  margin_percentage: float

  class Config:
    json_schema_extra = {
      "example": {
        "product_id": 1,
        "total_units": 42,
        "revenue": 126000.0,
        "total_cost": 42000.0,
        "gross_profit": 84000.0,
        "margin_percentage": 66.67
      }
    }


class ProductMarginListResponse(BaseModel):
  """Lista de márgenes por producto"""
  products: List[ProductMarginResponse]
  total: int

  class Config:
    json_schema_extra = {
      "example": {
        "products": [],
        "total": 0
      }
    }


# ==========================================
# RESPONSES - WASTE
# ==========================================

class WasteRatioResponse(BaseModel):
  """Ratio de desperdicio"""
  waste_cost: float = Field(description="Costo total de desperdicio")
  consumption_cost: float = Field(description="Costo de consumo")
  total_cost: float = Field(description="Costo total")
  waste_ratio_percentage: float = Field(description="Porcentaje de desperdicio")

  class Config:
    json_schema_extra = {
      "example": {
        "waste_cost": 2250.0,
        "consumption_cost": 42750.0,
        "total_cost": 45000.0,
        "waste_ratio_percentage": 5.0
      }
    }


# ==========================================
# RESPONSES - SALES SUMMARY
# ==========================================

class DailySalesResponse(BaseModel):
  """Resumen de ventas del día"""
  date: str
  total_sales: int = Field(description="Cantidad de ventas")
  total_revenue: float
  total_units: int = Field(description="Unidades vendidas")
  avg_sale: float = Field(description="Promedio por venta")

  class Config:
    json_schema_extra = {
      "example": {
        "date": "2026-05-18",
        "total_sales": 42,
        "total_revenue": 126000.0,
        "total_units": 150,
        "avg_sale": 3000.0
      }
    }


class TurnSalesResponse(BaseModel):
  """Resumen de ventas por turno"""
  turn_id: int
  turn_label: Optional[str] = None
  total_sales: int
  total_revenue: float
  total_units: int
  avg_sale: float

  class Config:
    json_schema_extra = {
      "example": {
        "turn_id": 1,
        "turn_label": "Mañana",
        "total_sales": 20,
        "total_revenue": 60000.0,
        "total_units": 75,
        "avg_sale": 3000.0
      }
    }


class EmployeeSalesResponse(BaseModel):
  """Resumen de ventas por empleado"""
  employee_id: int
  employee_name: Optional[str] = None
  total_sales: int
  total_revenue: float
  total_units: int
  avg_sale: float

  class Config:
    json_schema_extra = {
      "example": {
        "employee_id": 1,
        "employee_name": "Juan Pérez",
        "total_sales": 20,
        "total_revenue": 60000.0,
        "total_units": 75,
        "avg_sale": 3000.0
      }
    }


# ==========================================
# RESPONSES - DASHBOARD MAIN
# ==========================================

class DashboardMetricsResponse(BaseModel):
  """Métricas principales del dashboard"""
  total_revenue: float
  total_cogs: float
  gross_profit: float
  gross_margin_percentage: float
  waste_cost: float
  waste_ratio_percentage: float
  total_sales: int
  active_products: int

  class Config:
    json_schema_extra = {
      "example": {
        "total_revenue": 125000.0,
        "total_cogs": 45000.0,
        "gross_profit": 80000.0,
        "gross_margin_percentage": 64.0,
        "waste_cost": 2250.0,
        "waste_ratio_percentage": 5.0,
        "total_sales": 42,
        "active_products": 12
      }
    }
