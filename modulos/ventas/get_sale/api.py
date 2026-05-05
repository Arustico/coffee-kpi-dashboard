from fastapi import APIRouter

from .service import (
    execute_get_sale,
    execute_get_sales
)

from .schemas import SaleResponse

router = APIRouter()


# -------------------
# Lista de ventas
# -------------------
@router.get(
  "/sale",
  response_model=list[SaleResponse]
)
def get_sales_route():
  return execute_get_sales()


# -------------------
# Venta por ID
# -------------------
@router.get(
  "/sale/{sale_id}",
  response_model=SaleResponse
)
def get_sale_route(sale_id: int):
  return execute_get_sale(sale_id)



