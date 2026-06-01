from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ==========================================
# REQUESTS
# ==========================================

class WasteLogCreate(BaseModel):
  """Datos para registrar merma"""
  ingredient_id: int = Field(gt=0, description="ID del ingrediente")
  employee_id: int = Field(gt=0, description="ID del empleado que registra")
  turn_id: int = Field(gt=0, description="ID del turno")
  quantity: float = Field(gt=0, description="Cantidad de merma")
  reason: Optional[str] = Field(None, max_length=255, description="Motivo de la merma")

  class Config:
    json_schema_extra = {
      "example": {
        "ingredient_id": 1,
        "employee_id": 1,
        "turn_id": 1,
        "quantity": 50.0,
        "reason": "Vencimiento de producto"
      }
    }


class DateRangeFilterRequest(BaseModel):
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
# RESPONSES
# ==========================================

class WasteLogResponse(BaseModel):
  """Respuesta de registro de merma"""
  id: int
  ingredient_id: int
  employee_id: int
  turn_id: int
  logged_at: datetime
  quantity: float
  reason: Optional[str] = None

  class Config:
    from_attributes = True
    json_schema_extra = {
      "example": {
        "id": 1,
        "ingredient_id": 1,
        "employee_id": 1,
        "turn_id": 1,
        "logged_at": "2026-05-18T10:30:00",
        "quantity": 50.0,
        "reason": "Vencimiento de producto"
      }
    }


class WasteLogListResponse(BaseModel):
  """Lista de registros de merma"""
  waste_logs: List[WasteLogResponse]
  total: int

  class Config:
    json_schema_extra = {
      "example": {
        "waste_logs": [],
        "total": 0
      }
    }


class WasteLogCreateResponse(BaseModel):
  """Respuesta al registrar merma"""
  message: str
  waste_id: int
  quantity: float
  reason: Optional[str] = None

  class Config:
    json_schema_extra = {
      "example": {
        "message": "Merma registrada exitosamente",
        "waste_id": 1,
        "quantity": 50.0,
        "reason": "Vencimiento de producto"
      }
    }


class WasteLogDeleteResponse(BaseModel):
  """Respuesta al eliminar registro de merma"""
  message: str
  waste_id: int

  class Config:
    json_schema_extra = {
      "example": {
        "message": "Registro de merma eliminado exitosamente",
        "waste_id": 1
      }
    }


class WasteAnalyticsResponse(BaseModel):
  """Análisis de merma"""
  total_waste_quantity: float
  total_waste_cost: float
  waste_ratio: float = Field(description="Porcentaje de desperdicio")

  class Config:
    json_schema_extra = {
      "example": {
        "total_waste_quantity": 150.0,
        "total_waste_cost": 225.00,
        "waste_ratio": 5.5
      }
    }


class WasteIngredientAnalyticsResponse(BaseModel):
  """Análisis de merma por ingrediente"""
  ingredient_id: int
  ingredient_name: str
  unit: str
  total_quantity: float
  total_cost: float

  class Config:
    json_schema_extra = {
      "example": {
        "ingredient_id": 1,
        "ingredient_name": "Leche",
        "unit": "ml",
        "total_quantity": 150.0,
        "total_cost": 225.00
      }
    }


class WasteReasonSummaryResponse(BaseModel):
  """Resumen de merma por motivo"""
  reason: str
  count: int
  total_quantity: float

  class Config:
    json_schema_extra = {
      "example": {
        "reason": "Vencimiento de producto",
        "count": 5,
        "total_quantity": 250.0
      }
    }


class WasteRatioResponse(BaseModel):
  """Ratio de desperdicio"""
  waste_cost: float
  consumption_cost: float
  total_cost: float
  waste_ratio: float = Field(description="Porcentaje de desperdicio")

  class Config:
    json_schema_extra = {
      "example": {
        "waste_cost": 225.00,
        "consumption_cost": 4050.00,
        "total_cost": 4275.00,
        "waste_ratio": 5.26
      }
    }
