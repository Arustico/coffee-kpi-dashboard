
from fastapi import FastAPI
from modulos.ventas.create_sale.api import router as sales_router

app = FastAPI()

app.include_router(sales_router)
