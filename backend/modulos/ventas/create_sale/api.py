from fastapi import APIRouter
from .schemas import SaleCreate
from .service import create_sale

#--------------------------------------
# API ventas/create_sale
#--------------------------------------

router = APIRouter(prefix="/ventas", tags=["ventas"])

@router.post(
  "/crea_venta",
  status_code=201,
  summary="Registra una venta",
  description="Sólo empleados"
)
def create_sale_endpoint(data: SaleCreate):
  return create_sale(data)

