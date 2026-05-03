from pydantic import BaseModel, Field
from typing import List

"""
Definición de cómo llega la venta. Valida los datos de lo contrario arroja un error.
"""

class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int

class SaleCreate(BaseModel):
    employee_id: int
    turn_id: int
    items: List[SaleItemCreate]
