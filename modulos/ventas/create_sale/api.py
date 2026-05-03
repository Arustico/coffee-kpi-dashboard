from fastapi import APIRouter
from .schemas import SaleCreate
from .service import create_sale

router = APIRouter()

@router.post("/ventas")
def create_sale_endpoint(data: SaleCreate):
    return create_sale(data)
