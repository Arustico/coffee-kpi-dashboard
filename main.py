#-------------------------
# Librerias mínimas
#-------------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#-------------------------
# Routers
#-------------------------
# Logins
from modulos.auth.register.api import router as register_router
from modulos.auth.login.api import router as login_router
from modulos.auth.refresh.api import router as refresh_router

# Ventas
from modulos.ventas.create_sale.api import router as create_sales_router
from modulos.ventas.get_sale.api import router as get_sale_router

#-------------------------
# Inicio app:
#-------------------------
app = FastAPI(
	title="Coffee KPI Dashboard API",
	description="API para gestión de datos y KPIs para cafetería",
	version="0.1.0",
	contact={"name": "Ariel Nuñez Salinas", "contact":"ariel.nunez.sa@protonmail.com"}
	)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],#, "PUT", "DELETE"],
    allow_headers=["*"], #["Content-Type", "Authorization", "X-Requested-With"],
)


# Include routers
app.include_router(register_router)
app.include_router(login_router)
app.include_router(refresh_router)
app.include_router(create_sales_router)
app.include_router(get_sale_router)

# Mensaje
@app.get("/")
def read_root():
    return {"message": "Coffee KPI Dashboard API v0.1.0"}

