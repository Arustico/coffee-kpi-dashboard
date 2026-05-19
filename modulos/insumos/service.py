"""
SERVICE LAYER - Ingredient Purchases
Lógica de negocio, validaciones, transacciones
"""

from fastapi import HTTPException
from shared.database import get_connection
from modulos.insumos.repository import (
  create_supplier, get_supplier_by_id, get_all_suppliers,
  supplier_exists, get_supplier_by_name, supplier_name_exists,
  get_ingredient_by_id, get_all_ingredients,
  ingredient_exists, ingredient_is_active,
  ingredient_unit_exists, get_ingredient_unit,
  create_ingredient_purchase, get_purchase_by_id, get_all_purchases,
  get_purchases_by_ingredient, get_purchases_by_supplier,
  get_purchases_by_date_range, delete_purchase,
  get_total_purchase_amount, get_ingredient_stock_cost
)
from modulos.insumos.schemas import (
  SupplierCreate, SupplierResponse, SupplierListResponse, SupplierCreateResponse,
  IngredientResponse, IngredientListResponse, IngredientUnitResponse,
  IngredientPurchaseCreate, IngredientPurchaseResponse, IngredientPurchaseListResponse,
  PurchaseCreateResponse, PurchaseDeleteResponse, IngredientStockResponse,
  PurchaseDateFilterRequest
)
import logging

logger = logging.getLogger(__name__)


# ==========================================
# SUPPLIER SERVICES
# ==========================================

def create_supplier_service(data: SupplierCreate, admin_user):
  """Crea un nuevo proveedor"""
  conn = get_connection()

  try:
    conn.execute("BEGIN")
    logger.info(f"Iniciando creación de proveedor: {data.name}")

    # Validar que el nombre no exista
    if supplier_name_exists(conn, data.name):
      logger.warning(f"Proveedor duplicado: {data.name}")
      conn.rollback()
      raise HTTPException(
        status_code=400,
        detail="Proveedor ya existe"
      )

    # Crear proveedor
    supplier_id = create_supplier(conn, data.name)
    logger.info(f"Proveedor creado: {supplier_id}")

    conn.commit()

    return SupplierCreateResponse(
      message="Proveedor creado exitosamente",
      supplier_id=supplier_id
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al crear proveedor: {str(e)}", exc_info=True)
    try:
      conn.rollback()
    except:
      pass
    raise HTTPException(
      status_code=500,
      detail="Error al crear proveedor"
    )
  finally:
    conn.close()


def get_all_suppliers_service():
  """Obtiene lista de todos los proveedores"""
  conn = get_connection()

  try:
    suppliers_rows = get_all_suppliers(conn)

    suppliers = [
      SupplierResponse(
        id=row["id"],
        name=row["name"]
      )
      for row in suppliers_rows
    ]

    logger.info(f"Proveedores listados: {len(suppliers)}")

    return SupplierListResponse(
      suppliers=suppliers,
      total=len(suppliers)
    )

  except Exception as e:
    logger.error(f"Error al obtener proveedores: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener proveedores"
    )
  finally:
    conn.close()


def get_supplier_service(supplier_id: int):
  """Obtiene un proveedor específico"""
  conn = get_connection()

  try:
    supplier = get_supplier_by_id(conn, supplier_id)

    if supplier is None:
      logger.warning(f"Proveedor no encontrado: {supplier_id}")
      raise HTTPException(
        status_code=404,
        detail="Proveedor no encontrado"
      )

    return SupplierResponse(
      id=supplier["id"],
      name=supplier["name"]
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al obtener proveedor: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener proveedor"
    )
  finally:
    conn.close()


# ==========================================
# INGREDIENT SERVICES
# ==========================================

def get_all_ingredients_service():
  """Obtiene lista de todos los ingredientes activos"""
  conn = get_connection()

  try:
    ingredients_rows = get_all_ingredients(conn)

    ingredients = [
      IngredientResponse(
        id=row["id"],
        name=row["name"],
        unit=row["unit"],
        active=bool(row["active"])
      )
      for row in ingredients_rows
    ]

    logger.info(f"Ingredientes listados: {len(ingredients)}")

    return IngredientListResponse(
      ingredients=ingredients,
      total=len(ingredients)
    )

  except Exception as e:
    logger.error(f"Error al obtener ingredientes: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener ingredientes"
    )
  finally:
    conn.close()


def get_ingredient_service(ingredient_id: int):
  """Obtiene un ingrediente específico"""
  conn = get_connection()

  try:
    ingredient = get_ingredient_by_id(conn, ingredient_id)

    if ingredient is None:
      logger.warning(f"Ingrediente no encontrado: {ingredient_id}")
      raise HTTPException(
        status_code=404,
        detail="Ingrediente no encontrado"
      )

    return IngredientResponse(
      id=ingredient["id"],
      name=ingredient["name"],
      unit=ingredient["unit"],
      active=bool(ingredient["active"])
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al obtener ingrediente: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener ingrediente"
    )
  finally:
    conn.close()


def get_ingredient_stock_service(ingredient_id: int):
  """Obtiene el stock y costo promedio de un ingrediente"""
  conn = get_connection()

  try:
    # Validar que ingrediente existe
    ingredient = get_ingredient_by_id(conn, ingredient_id)
    if ingredient is None:
      logger.warning(f"Ingrediente no encontrado: {ingredient_id}")
      raise HTTPException(
        status_code=404,
        detail="Ingrediente no encontrado"
      )

    # Obtener stock
    stock_data = get_ingredient_stock_cost(conn, ingredient_id)

    logger.info(f"Stock de ingrediente obtenido: {ingredient_id}")

    return IngredientStockResponse(
      ingredient_id=ingredient["id"],
      ingredient_name=ingredient["name"],
      unit=ingredient["unit"],
      total_quantity=stock_data["total_quantity"],
      avg_cost=stock_data["avg_cost"]
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al obtener stock: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener stock"
    )
  finally:
    conn.close()


# ==========================================
# PURCHASE SERVICES
# ==========================================

def create_purchase_service(data: IngredientPurchaseCreate):
  """Crea una nueva compra de ingrediente"""
  conn = get_connection()

  try:
    conn.execute("BEGIN")
    logger.info(f"Iniciando compra de ingrediente: {data.ingredient_id}")

    # Validar que ingrediente existe
    if not ingredient_exists(conn, data.ingredient_id):
      logger.warning(f"Ingrediente no existe: {data.ingredient_id}")
      conn.rollback()
      raise HTTPException(
        status_code=404,
        detail="Ingrediente no encontrado"
      )

    # Validar que ingrediente está activo
    if not ingredient_is_active(conn, data.ingredient_id):
      logger.warning(f"Ingrediente inactivo: {data.ingredient_id}")
      conn.rollback()
      raise HTTPException(
        status_code=400,
        detail="Ingrediente inactivo"
      )

    # Validar proveedor si se proporciona
    if data.supplier_id is not None:
      if not supplier_exists(conn, data.supplier_id):
        logger.warning(f"Proveedor no existe: {data.supplier_id}")
        conn.rollback()
        raise HTTPException(
          status_code=404,
          detail="Proveedor no encontrado"
        )

    # Crear compra
    try:
      purchase_id = create_ingredient_purchase(
        conn,
        ingredient_id=data.ingredient_id,
        quantity=data.quantity,
        unit_cost=data.unit_cost,
        supplier_id=data.supplier_id
      )

      total_amount = data.quantity * data.unit_cost
      logger.info(f"Compra creada: {purchase_id}, total: {total_amount}")
    except Exception as e:
      logger.error(f"Error al crear compra: {str(e)}")
      conn.rollback()
      raise HTTPException(
        status_code=500,
        detail="Error al crear compra"
      )

    conn.commit()

    return PurchaseCreateResponse(
      message="Compra creada exitosamente",
      purchase_id=purchase_id,
      total_amount=total_amount
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error inesperado al crear compra: {str(e)}", exc_info=True)
    try:
      conn.rollback()
    except:
      pass
    raise HTTPException(
      status_code=500,
      detail="Error al crear compra"
    )
  finally:
    conn.close()


def get_all_purchases_service():
  """Obtiene lista de todas las compras"""
  conn = get_connection()

  try:
    purchases_rows = get_all_purchases(conn)

    purchases = []
    total_amount = 0.0

    for row in purchases_rows:
      item_total = row["quantity"] * row["unit_cost"]
      total_amount += item_total

      purchases.append(
        IngredientPurchaseResponse(
          id=row["id"],
          ingredient_id=row["ingredient_id"],
          supplier_id=row["supplier_id"],
          quantity=row["quantity"],
          unit_cost=row["unit_cost"],
          purchased_at=row["purchased_at"],
          total_amount=item_total
        )
      )

    logger.info(f"Compras listadas: {len(purchases)}")

    return IngredientPurchaseListResponse(
      purchases=purchases,
      total=len(purchases),
      total_amount=total_amount
    )

  except Exception as e:
    logger.error(f"Error al obtener compras: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener compras"
    )
  finally:
    conn.close()


def get_purchase_service(purchase_id: int):
  """Obtiene una compra específica"""
  conn = get_connection()

  try:
    purchase = get_purchase_by_id(conn, purchase_id)

    if purchase is None:
      logger.warning(f"Compra no encontrada: {purchase_id}")
      raise HTTPException(
        status_code=404,
        detail="Compra no encontrada"
      )

    total_amount = purchase["quantity"] * purchase["unit_cost"]

    return IngredientPurchaseResponse(
      id=purchase["id"],
      ingredient_id=purchase["ingredient_id"],
      supplier_id=purchase["supplier_id"],
      quantity=purchase["quantity"],
      unit_cost=purchase["unit_cost"],
      purchased_at=purchase["purchased_at"],
      total_amount=total_amount
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al obtener compra: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener compra"
    )
  finally:
    conn.close()


def get_purchases_by_ingredient_service(ingredient_id: int):
  """Obtiene compras de un ingrediente específico"""
  conn = get_connection()

  try:
    # Validar que ingrediente existe
    if not ingredient_exists(conn, ingredient_id):
      logger.warning(f"Ingrediente no existe: {ingredient_id}")
      raise HTTPException(
        status_code=404,
        detail="Ingrediente no encontrado"
      )

    purchases_rows = get_purchases_by_ingredient(conn, ingredient_id)

    purchases = []
    total_amount = 0.0

    for row in purchases_rows:
      item_total = row["quantity"] * row["unit_cost"]
      total_amount += item_total

      purchases.append(
        IngredientPurchaseResponse(
          id=row["id"],
          ingredient_id=row["ingredient_id"],
          supplier_id=row["supplier_id"],
          quantity=row["quantity"],
          unit_cost=row["unit_cost"],
          purchased_at=row["purchased_at"],
          total_amount=item_total
        )
      )

    logger.info(f"Compras por ingrediente: {len(purchases)}")

    return IngredientPurchaseListResponse(
      purchases=purchases,
      total=len(purchases),
      total_amount=total_amount
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al obtener compras: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener compras"
    )
  finally:
    conn.close()


def get_purchases_by_supplier_service(supplier_id: int):
  """Obtiene compras de un proveedor específico"""
  conn = get_connection()

  try:
    # Validar que proveedor existe
    if not supplier_exists(conn, supplier_id):
      logger.warning(f"Proveedor no existe: {supplier_id}")
      raise HTTPException(
        status_code=404,
        detail="Proveedor no encontrado"
      )

    purchases_rows = get_purchases_by_supplier(conn, supplier_id)

    purchases = []
    total_amount = 0.0

    for row in purchases_rows:
      item_total = row["quantity"] * row["unit_cost"]
      total_amount += item_total

      purchases.append(
        IngredientPurchaseResponse(
          id=row["id"],
          ingredient_id=row["ingredient_id"],
          supplier_id=row["supplier_id"],
          quantity=row["quantity"],
          unit_cost=row["unit_cost"],
          purchased_at=row["purchased_at"],
          total_amount=item_total
        )
      )

    logger.info(f"Compras por proveedor: {len(purchases)}")

    return IngredientPurchaseListResponse(
      purchases=purchases,
      total=len(purchases),
      total_amount=total_amount
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al obtener compras: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener compras"
    )
  finally:
    conn.close()


def get_purchases_by_date_range_service(data: PurchaseDateFilterRequest):
  """Obtiene compras en un rango de fechas"""
  conn = get_connection()

  try:
    purchases_rows = get_purchases_by_date_range(conn, data.start_date, data.end_date)

    purchases = []
    total_amount = 0.0

    for row in purchases_rows:
      item_total = row["quantity"] * row["unit_cost"]
      total_amount += item_total

      purchases.append(
        IngredientPurchaseResponse(
          id=row["id"],
          ingredient_id=row["ingredient_id"],
          supplier_id=row["supplier_id"],
          quantity=row["quantity"],
          unit_cost=row["unit_cost"],
          purchased_at=row["purchased_at"],
          total_amount=item_total
        )
      )

    logger.info(f"Compras por rango de fechas: {len(purchases)}")

    return IngredientPurchaseListResponse(
      purchases=purchases,
      total=len(purchases),
      total_amount=total_amount
    )

  except Exception as e:
    logger.error(f"Error al obtener compras: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener compras"
    )
  finally:
    conn.close()


def delete_purchase_service(purchase_id: int):
  """Elimina una compra"""
  conn = get_connection()

  try:
    conn.execute("BEGIN")

    # Verificar que existe
    purchase = get_purchase_by_id(conn, purchase_id)
    if purchase is None:
      conn.rollback()
      logger.warning(f"Compra no encontrada: {purchase_id}")
      raise HTTPException(
        status_code=404,
        detail="Compra no encontrada"
      )

    # Eliminar
    delete_purchase(conn, purchase_id)

    conn.commit()
    logger.info(f"Compra eliminada: {purchase_id}")

    return PurchaseDeleteResponse(
      message="Compra eliminada exitosamente",
      purchase_id=purchase_id
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al eliminar compra: {str(e)}")
    try:
      conn.rollback()
    except:
      pass
    raise HTTPException(
      status_code=500,
      detail="Error al eliminar compra"
    )
  finally:
    conn.close()
