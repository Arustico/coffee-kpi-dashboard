from pydantic import BaseModel, Field
from typing import List, Optional

"""
Definición de cómo llega la venta. Valida los datos de lo contrario arroja un error.
  Contrains: Ventas mayor a 0 y menores o iguales a 99
"""

class SaleItemCreate(BaseModel):
  product_id: int
  quantity: int = Field(gt=0, le=99)

class SaleCreate(BaseModel):
  employee_id: int = Field(gt=0, le=9)
  turn_id: Optional[int] = None
  items: List[SaleItemCreate]

