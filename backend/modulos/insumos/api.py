"""
API LAYER - Insumos/Ingredient Purchases
Rutas HTTP
"""

from fastapi import APIRouter, Depends
from shared.security.dependencies import get_current_user, get_current_admin
from modulos.insumos.schemas import (
  SupplierCreate, SupplierResponse, SupplierListResponse, SupplierCreateResponse,
  IngredientResponse, IngredientListResponse,
  IngredientPurchaseCreate, IngredientPurchaseResponse, IngredientPurchaseListResponse,
  PurchaseCreateResponse, PurchaseDeleteResponse, IngredientStockResponse,
  PurchaseDateFilterRequest, ProductListResponse
)
from modulos.insumos.service import (
  create_supplier_service, get_all_suppliers_service, get_supplier_service,
  get_all_ingredients_service, get_ingredient_service, get_ingredient_stock_service,
  get_all_products_service,
  create_purchase_service, get_all_purchases_service, get_purchase_service,
  get_purchases_by_ingredient_service, get_purchases_by_supplier_service,
  get_purchases_by_date_range_service, delete_purchase_service
)

router = APIRouter(prefix="/ingredients", tags=["ingredients"])

#---------------------------------------------
#  API INSUMOS MODULE
#---------------------------------------------

# ==========================================
# SUPPLIERS
# ==========================================

@router.post(
  "/suppliers",
  response_model=SupplierCreateResponse,
  status_code=201,
  summary="Crear proveedor",
  description="Solo administradores"
)
def create_supplier(
  data: SupplierCreate,
  admin = Depends(get_current_admin)
):
  """Crea un nuevo proveedor"""
  return create_supplier_service(data, admin)


@router.get(
  "/suppliers",
  response_model=SupplierListResponse,
  summary="Listar proveedores",
  description="Obtiene lista de todos los proveedores"
)
def list_suppliers(current_user = Depends(get_current_user)):
  """Obtiene lista de todos los proveedores"""
  return get_all_suppliers_service()


@router.get(
  "/suppliers/{supplier_id}",
  response_model=SupplierResponse,
  summary="Obtener proveedor",
  description="Obtiene un proveedor específico"
)
def get_supplier(
  supplier_id: int,
  current_user = Depends(get_current_user)
):
  """Obtiene los detalles de un proveedor"""
  return get_supplier_service(supplier_id)


# ==========================================
# INGREDIENTS
# ==========================================

@router.get(
  "",
  response_model=IngredientListResponse,
  summary="Listar ingredientes",
  description="Obtiene lista de todos los ingredientes activos"
)
def list_ingredients(current_user = Depends(get_current_user)):
  """Obtiene lista de todos los ingredientes"""
  return get_all_ingredients_service()


# ==========================================
# PRODUCTS
# ==========================================

@router.get(
  "/products",
  response_model=ProductListResponse,
  summary="Listar productos",
  description="Obtiene lista de todos los productos activos"
)
def list_products(current_user = Depends(get_current_user)):
  """Obtiene lista de todos los productos"""
  return get_all_products_service()


@router.get(
  "/{ingredient_id}",
  response_model=IngredientResponse,
  summary="Obtener ingrediente",
  description="Obtiene un ingrediente específico"
)
def get_ingredient(
  ingredient_id: int,
  current_user = Depends(get_current_user)
):
  """Obtiene los detalles de un ingrediente"""
  return get_ingredient_service(ingredient_id)


@router.get(
  "/{ingredient_id}/stock",
  response_model=IngredientStockResponse,
  summary="Obtener stock de ingrediente",
  description="Obtiene stock y costo promedio de un ingrediente"
)
def get_ingredient_stock(
  ingredient_id: int,
  current_user = Depends(get_current_user)
):
  """Obtiene el stock y costo promedio de un ingrediente basado en compras históricas"""
  return get_ingredient_stock_service(ingredient_id)


# ==========================================
# PURCHASES
# ==========================================

@router.post(
  "/purchases",
  response_model=PurchaseCreateResponse,
  status_code=201,
  summary="Crear compra de ingrediente",
  description="Registra una nueva compra de ingrediente"
)
def create_purchase(
  data: IngredientPurchaseCreate,
  current_user = Depends(get_current_user)
):
  """
  Crea una nueva compra de ingrediente

  - **ingredient_id**: ID del ingrediente (requerido)
  - **quantity**: Cantidad comprada (requerido)
  - **unit_cost**: Costo unitario (requerido)
  - **supplier_id**: ID del proveedor (opcional)
  """
  return create_purchase_service(data)


@router.get(
  "/purchases",
  response_model=IngredientPurchaseListResponse,
  summary="Listar compras",
  description="Obtiene lista de todas las compras de ingredientes"
)
def list_purchases(current_user = Depends(get_current_user)):
  """Obtiene lista de todas las compras"""
  return get_all_purchases_service()


@router.get(
  "/purchases/{purchase_id}",
  response_model=IngredientPurchaseResponse,
  summary="Obtener compra",
  description="Obtiene una compra específica"
)
def get_purchase(
  purchase_id: int,
  current_user = Depends(get_current_user)
):
  """Obtiene los detalles de una compra específica"""
  return get_purchase_service(purchase_id)


@router.get(
  "/purchases/by-ingredient/{ingredient_id}",
  response_model=IngredientPurchaseListResponse,
  summary="Compras por ingrediente",
  description="Obtiene compras de un ingrediente específico"
)
def get_purchases_by_ingredient(
  ingredient_id: int,
  current_user = Depends(get_current_user)
):
  """Obtiene todas las compras de un ingrediente específico"""
  return get_purchases_by_ingredient_service(ingredient_id)


@router.get(
  "/purchases/by-supplier/{supplier_id}",
  response_model=IngredientPurchaseListResponse,
  summary="Compras por proveedor",
  description="Obtiene compras de un proveedor específico"
)
def get_purchases_by_supplier(
  supplier_id: int,
  current_user = Depends(get_current_user)
):
  """Obtiene todas las compras de un proveedor específico"""
  return get_purchases_by_supplier_service(supplier_id)


@router.post(
  "/purchases/by-date-range",
  response_model=IngredientPurchaseListResponse,
  summary="Compras por rango de fechas",
  description="Obtiene compras en un rango de fechas"
)
def get_purchases_by_date_range(
  data: PurchaseDateFilterRequest,
  current_user = Depends(get_current_user)
):
  """
  Obtiene compras en un rango de fechas

  - **start_date**: Fecha inicio (YYYY-MM-DD)
  - **end_date**: Fecha fin (YYYY-MM-DD)
  """
  return get_purchases_by_date_range_service(data)


@router.delete(
  "/purchases/{purchase_id}",
  response_model=PurchaseDeleteResponse,
  summary="Eliminar compra",
  description="Solo administradores"
)
def delete_purchase(
  purchase_id: int,
  admin = Depends(get_current_admin)
):
  """Elimina una compra de ingrediente"""
  return delete_purchase_service(purchase_id)
