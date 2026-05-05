
from fastapi import FastAPI
from modulos.ventas.create_sale.api import router as create_sales_router
from modulos.ventas.get_sale.api import router as get_sale_router


app = FastAPI()

app.include_router(create_sales_router)
app.include_router(get_sale_router)
