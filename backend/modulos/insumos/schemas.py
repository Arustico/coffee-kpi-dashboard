# Librerías
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ------------------------------------------
# SCHEMAS INSUMOS
# ------------------------------------------

# ==========================================
# REQUESTS
# ==========================================

class SupplierCreate(BaseModel):
  """Datos para crear un proveedor"""
  name: str = Field(min_length=2, max_length=100, description="Nombre del proveedor")

  class Config:
    json_schema_extra = {
      "example": {
        "name": "Proveedor ABC"
      }
    }


class IngredientPurchaseCreate(BaseModel):
  """Datos para crear una compra de ingrediente"""
  ingredient_id: int = Field(gt=0, description="ID del ingrediente")
  quantity: float = Field(gt=0, description="Cantidad comprada")
  unit_cost: float = Field(ge=0, description="Costo unitario")
  supplier_id: Optional[int] = Field(None, description="ID del proveedor (opcional)")

  class Config:
    json_schema_extra = {
      "example": {
        "ingredient_id": 1,
        "quantity": 100.0,
        "unit_cost": 1.50,
        "supplier_id": 1
      }
    }


class PurchaseDateFilterRequest(BaseModel):
  """Filtro de rango de fechas para compras"""
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

class IngredientUnitResponse(BaseModel):
  """Respuesta de unidad de medida"""
  unit: str
  description: Optional[str] = None

  class Config:
    from_attributes = True


class IngredientResponse(BaseModel):
  """Respuesta de ingrediente"""
  id: int
  name: str
  unit: str
  active: bool

  class Config:
    from_attributes = True
    json_schema_extra = {
      "example": {
        "id": 1,
        "name": "Leche",
        "unit": "ml",
        "active": True
      }
    }


class IngredientListResponse(BaseModel):
  """Lista de ingredientes"""
  ingredients: List[IngredientResponse]
  total: int

  class Config:
    json_schema_extra = {
      "example": {
        "ingredients": [],
        "total": 0
      }
    }


class SupplierResponse(BaseModel):
  """Respuesta de proveedor"""
  id: int
  name: str

  class Config:
    from_attributes = True
    json_schema_extra = {
      "example": {
        "id": 1,
        "name": "Proveedor ABC"
      }
    }


class SupplierListResponse(BaseModel):
  """Lista de proveedores"""
  suppliers: List[SupplierResponse]
  total: int

  class Config:
    json_schema_extra = {
      "example": {
        "suppliers": [],
        "total": 0
      }
    }


class SupplierCreateResponse(BaseModel):
  """Respuesta al crear proveedor"""
  message: str
  supplier_id: int

  class Config:
    json_schema_extra = {
      "example": {
        "message": "Proveedor creado exitosamente",
        "supplier_id": 1
      }
    }


class IngredientPurchaseResponse(BaseModel):
  """Respuesta de compra de ingrediente"""
  id: int
  ingredient_id: int
  supplier_id: Optional[int] = None
  quantity: float
  unit_cost: float
  purchased_at: datetime
  total_amount: float = Field(description="quantity * unit_cost")

  class Config:
    from_attributes = True
    json_schema_extra = {
      "example": {
        "id": 1,
        "ingredient_id": 1,
        "supplier_id": 1,
        "quantity": 100.0,
        "unit_cost": 1.50,
        "purchased_at": "2026-05-18T10:30:00",
        "total_amount": 150.0
      }
    }


class IngredientPurchaseListResponse(BaseModel):
  """Lista de compras de ingredientes"""
  purchases: List[IngredientPurchaseResponse]
  total: int
  total_amount: float = Field(description="Monto total de todas las compras")

  class Config:
    json_schema_extra = {
      "example": {
        "purchases": [],
        "total": 0,
        "total_amount": 0.0
      }
    }


class PurchaseCreateResponse(BaseModel):
  """Respuesta al crear compra"""
  message: str
  purchase_id: int
  total_amount: float

  class Config:
    json_schema_extra = {
      "example": {
        "message": "Compra creada exitosamente",
        "purchase_id": 1,
        "total_amount": 150.0
      }
    }


class PurchaseDeleteResponse(BaseModel):
  """Respuesta al eliminar compra"""
  message: str
  purchase_id: int

  class Config:
    json_schema_extra = {
      "example": {
        "message": "Compra eliminada exitosamente",
        "purchase_id": 1
      }
    }


class ProductItemResponse(BaseModel):
  """Respuesta de producto"""
  id: int
  name: str
  base_price: float

  class Config:
    from_attributes = True


class ProductListResponse(BaseModel):
  """Lista de productos"""
  items: List[ProductItemResponse]
  total: int


class IngredientStockResponse(BaseModel):
  """Respuesta de stock de ingrediente"""
  ingredient_id: int
  ingredient_name: str
  unit: str
  total_quantity: float
  avg_cost: float

  class Config:
    json_schema_extra = {
      "example": {
        "ingredient_id": 1,
        "ingredient_name": "Leche",
        "unit": "ml",
        "total_quantity": 500.0,
        "avg_cost": 1.50
      }
    }
