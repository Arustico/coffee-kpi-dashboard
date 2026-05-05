from pydantic import BaseModel, Field
from datetime import datetime


# Una sola venta
class SaleResponse(BaseModel):
  id: int
  sold_at: datetime
  total_amount: float = Field(gt=0)

# Lista de ventas
class SaleListResponse(BaseModel):
  sales: list[SaleResponse]
