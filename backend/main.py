#-------------------------
# Librerias mínimas
#-------------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Logs Errores
import logging
logger = logging.getLogger(__name__)


#-------------------------
# Routers
#-------------------------
# Logins
from modulos.auth.register.api import router as register_router
from modulos.auth.login.api import router as login_router
from modulos.auth.refresh.api import router as refresh_router
from modulos.auth.users.api import router as users_router
from modulos.employees.api import router as employees_router

# Ventas
from modulos.ventas.create_sale.api import router as create_sales_router
from modulos.ventas.get_sale.api import router as get_sale_router
# Insumos
from modulos.insumos.api import router as ingredients_router
# Merma
from modulos.merma.api import router as merma_router
# Kpis
from modulos.KPIs.api import router as kpis_router
# Roles
from modulos.roles.api import router as roles_router

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
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):(517[3-6]|3000|8080|8000)",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"], #["Content-Type", "Authorization", "X-Requested-With"],
)


# Include routers
logger.info("Cargando routers...")
app.include_router(register_router)
app.include_router(login_router)
app.include_router(users_router)
app.include_router(employees_router)
app.include_router(refresh_router)
app.include_router(create_sales_router)
app.include_router(get_sale_router)
app.include_router(ingredients_router)
app.include_router(merma_router)
app.include_router(kpis_router)
app.include_router(roles_router)
logger.info("Routers cargadas con éxito!")

# Mensaje
@app.get("/")
def read_root():
    return {"message": "Coffee KPI Dashboard API v0.1.0"}

