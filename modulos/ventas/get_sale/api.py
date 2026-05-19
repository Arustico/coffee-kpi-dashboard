
from fastapi import APIRouter
from .service import execute_get_sale, execute_get_sales
from .schemas import SaleResponse


#--------------------------------------
# API ventas/get_sale
#--------------------------------------

router = APIRouter(prefix="/ventas", tags=["ventas"])


#--------------------------------------
# Lista de ventas
#--------------------------------------
@router.get(
  "/sale",
  response_model=list[SaleResponse],
  summary="Consulta toda las ventas",
  description="Usuarios del dashboard"
)
def get_sales_route():
  return execute_get_sales()


# -------------------
# Venta por ID
# -------------------
@router.get(
  "/sale/{sale_id}",
  response_model=SaleResponse,
  summary="Consulta por una venta en particular",
  description="Usuarios del dashboard"
)
def get_sale_route(sale_id: int):
  return execute_get_sale(sale_id)



