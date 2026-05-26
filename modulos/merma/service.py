"""
SERVICE LAYER - Waste Logging
Lógica de negocio, validaciones, transacciones
"""

from fastapi import HTTPException
from shared.database import get_connection
from modulos.merma.repository import (
  create_waste_log, get_waste_log_by_id, get_all_waste_logs,
  get_waste_logs_by_ingredient, get_waste_logs_by_employee,
  get_waste_logs_by_turn, get_waste_logs_by_date_range,
  delete_waste_log, get_total_waste_by_ingredient,
  get_total_waste_by_date_range, get_waste_cost_by_ingredient,
  get_total_waste_cost, get_waste_ratio_by_date_range,
  get_waste_reasons_summary
)
from modulos.merma.schemas import (
  WasteLogCreate, WasteLogResponse, WasteLogListResponse,
  WasteLogCreateResponse, WasteLogDeleteResponse,
  WasteAnalyticsResponse, WasteIngredientAnalyticsResponse,
  WasteRatioResponse, DateRangeFilterRequest, WasteReasonSummaryResponse
)
from modulos.insumos.repository import (
  ingredient_exists, ingredient_is_active, get_ingredient_by_id,
  get_ingredient_stock_cost
)
from modulos.auth.repository.user_repository import (
  employee_exists, employee_is_active
)
from modulos.ventas.repository import get_turn_by_id
import logging

logger = logging.getLogger(__name__)


def create_waste_log_service(data: WasteLogCreate):
  """Registra una nueva merma"""
  conn = get_connection()

  try:
    conn.execute("BEGIN")
    logger.info(f"Iniciando registro de merma para ingrediente: {data.ingredient_id}")

    # ========== VALIDACIONES ==========

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

    # Validar que empleado existe
    if not employee_exists(conn, data.employee_id):
      logger.warning(f"Empleado no existe: {data.employee_id}")
      conn.rollback()
      raise HTTPException(
        status_code=404,
        detail="Empleado no encontrado"
      )

    # Validar que empleado está activo
    if not employee_is_active(conn, data.employee_id):
      logger.warning(f"Empleado inactivo: {data.employee_id}")
      conn.rollback()
      raise HTTPException(
        status_code=400,
        detail="Empleado inactivo"
      )

    # Validar que turno existe
    turn = get_turn_by_id(conn, data.turn_id)
    if turn is None:
      logger.warning(f"Turno no existe: {data.turn_id}")
      conn.rollback()
      raise HTTPException(
        status_code=404,
        detail="Turno no encontrado"
      )

    # ========== PROCESAMIENTO ==========

    # Crear registro de merma
    try:
      waste_id = create_waste_log(
        conn,
        ingredient_id=data.ingredient_id,
        employee_id=data.employee_id,
        turn_id=data.turn_id,
        quantity=data.quantity,
        reason=data.reason
      )
      logger.info(f"Merma registrada: {waste_id}, cantidad: {data.quantity}")
    except Exception as e:
      logger.error(f"Error al registrar merma: {str(e)}")
      conn.rollback()
      raise HTTPException(
        status_code=500,
        detail="Error al registrar merma"
      )

    # ========== COMMIT TRANSACCIÓN ==========
    conn.commit()
    logger.info(f"Registro de merma completado: {waste_id}")

    return WasteLogCreateResponse(
      message="Merma registrada exitosamente",
      waste_id=waste_id,
      quantity=data.quantity,
      reason=data.reason
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error inesperado al registrar merma: {str(e)}", exc_info=True)
    try:
      conn.rollback()
    except:
      pass
    raise HTTPException(
      status_code=500,
      detail="Error al registrar merma"
    )
  finally:
    conn.close()


def get_all_waste_logs_service():
  """Obtiene lista de todos los registros de merma"""
  conn = get_connection()

  try:
    waste_logs_rows = get_all_waste_logs(conn)

    waste_logs = [
      WasteLogResponse(
        id=row["id"],
        ingredient_id=row["ingredient_id"],
        employee_id=row["employee_id"],
        turn_id=row["turn_id"],
        logged_at=row["logged_at"],
        quantity=row["quantity"],
        reason=row["reason"]
      )
      for row in waste_logs_rows
    ]

    logger.info(f"Registros de merma listados: {len(waste_logs)}")

    return WasteLogListResponse(
      waste_logs=waste_logs,
      total=len(waste_logs)
    )

  except Exception as e:
    logger.error(f"Error al obtener registros de merma: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener registros de merma"
    )
  finally:
    conn.close()


def get_waste_log_service(waste_id: int):
  """Obtiene un registro de merma específico"""
  conn = get_connection()

  try:
    waste_log = get_waste_log_by_id(conn, waste_id)

    if waste_log is None:
      logger.warning(f"Registro de merma no encontrado: {waste_id}")
      raise HTTPException(
        status_code=404,
        detail="Registro de merma no encontrado"
      )

    return WasteLogResponse(
      id=waste_log["id"],
      ingredient_id=waste_log["ingredient_id"],
      employee_id=waste_log["employee_id"],
      turn_id=waste_log["turn_id"],
      logged_at=waste_log["logged_at"],
      quantity=waste_log["quantity"],
      reason=waste_log["reason"]
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al obtener registro de merma: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener registro de merma"
    )
  finally:
    conn.close()


def get_waste_logs_by_ingredient_service(ingredient_id: int):
  """Obtiene registros de merma de un ingrediente"""
  conn = get_connection()

  try:
    # Validar que ingrediente existe
    if not ingredient_exists(conn, ingredient_id):
      logger.warning(f"Ingrediente no existe: {ingredient_id}")
      raise HTTPException(
        status_code=404,
        detail="Ingrediente no encontrado"
      )

    waste_logs_rows = get_waste_logs_by_ingredient(conn, ingredient_id)

    waste_logs = [
      WasteLogResponse(
        id=row["id"],
        ingredient_id=row["ingredient_id"],
        employee_id=row["employee_id"],
        turn_id=row["turn_id"],
        logged_at=row["logged_at"],
        quantity=row["quantity"],
        reason=row["reason"]
      )
      for row in waste_logs_rows
    ]

    logger.info(f"Registros de merma por ingrediente: {len(waste_logs)}")

    return WasteLogListResponse(
      waste_logs=waste_logs,
      total=len(waste_logs)
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al obtener registros: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener registros de merma"
    )
  finally:
    conn.close()


def get_waste_logs_by_employee_service(employee_id: int):
  """Obtiene registros de merma de un empleado"""
  conn = get_connection()

  try:
    # Validar que empleado existe
    if not employee_exists(conn, employee_id):
      logger.warning(f"Empleado no existe: {employee_id}")
      raise HTTPException(
        status_code=404,
        detail="Empleado no encontrado"
      )

    waste_logs_rows = get_waste_logs_by_employee(conn, employee_id)

    waste_logs = [
      WasteLogResponse(
        id=row["id"],
        ingredient_id=row["ingredient_id"],
        employee_id=row["employee_id"],
        turn_id=row["turn_id"],
        logged_at=row["logged_at"],
        quantity=row["quantity"],
        reason=row["reason"]
      )
      for row in waste_logs_rows
    ]

    logger.info(f"Registros de merma por empleado: {len(waste_logs)}")

    return WasteLogListResponse(
      waste_logs=waste_logs,
      total=len(waste_logs)
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al obtener registros: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener registros de merma"
    )
  finally:
    conn.close()


def get_waste_logs_by_turn_service(turn_id: int):
  """Obtiene registros de merma de un turno"""
  conn = get_connection()

  try:
    # Validar que turno existe
    turn = get_turn_by_id(conn, turn_id)
    if turn is None:
      logger.warning(f"Turno no existe: {turn_id}")
      raise HTTPException(
        status_code=404,
        detail="Turno no encontrado"
      )

    waste_logs_rows = get_waste_logs_by_turn(conn, turn_id)

    waste_logs = [
      WasteLogResponse(
        id=row["id"],
        ingredient_id=row["ingredient_id"],
        employee_id=row["employee_id"],
        turn_id=row["turn_id"],
        logged_at=row["logged_at"],
        quantity=row["quantity"],
        reason=row["reason"]
      )
      for row in waste_logs_rows
    ]

    logger.info(f"Registros de merma por turno: {len(waste_logs)}")

    return WasteLogListResponse(
      waste_logs=waste_logs,
      total=len(waste_logs)
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al obtener registros: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener registros de merma"
    )
  finally:
    conn.close()


def get_waste_logs_by_date_range_service(data: DateRangeFilterRequest):
  """Obtiene registros de merma en un rango de fechas"""
  conn = get_connection()

  try:
    waste_logs_rows = get_waste_logs_by_date_range(conn, data.start_date, data.end_date)

    waste_logs = [
      WasteLogResponse(
        id=row["id"],
        ingredient_id=row["ingredient_id"],
        employee_id=row["employee_id"],
        turn_id=row["turn_id"],
        logged_at=row["logged_at"],
        quantity=row["quantity"],
        reason=row["reason"]
      )
      for row in waste_logs_rows
    ]

    logger.info(f"Registros de merma por rango: {len(waste_logs)}")

    return WasteLogListResponse(
      waste_logs=waste_logs,
      total=len(waste_logs)
    )

  except Exception as e:
    logger.error(f"Error al obtener registros: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener registros de merma"
    )
  finally:
    conn.close()


def delete_waste_log_service(waste_id: int):
  """Elimina un registro de merma"""
  conn = get_connection()

  try:
    conn.execute("BEGIN")

    # Verificar que existe
    waste_log = get_waste_log_by_id(conn, waste_id)
    if waste_log is None:
      conn.rollback()
      logger.warning(f"Registro de merma no encontrado: {waste_id}")
      raise HTTPException(
        status_code=404,
        detail="Registro de merma no encontrado"
      )

    # Eliminar
    delete_waste_log(conn, waste_id)

    conn.commit()
    logger.info(f"Registro de merma eliminado: {waste_id}")

    return WasteLogDeleteResponse(
      message="Registro de merma eliminado exitosamente",
      waste_id=waste_id
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al eliminar registro: {str(e)}")
    try:
      conn.rollback()
    except:
      pass
    raise HTTPException(
      status_code=500,
      detail="Error al eliminar registro de merma"
    )
  finally:
    conn.close()


def get_waste_analytics_by_ingredient_service(ingredient_id: int):
  """Obtiene análisis de merma de un ingrediente"""
  conn = get_connection()

  try:
    # Validar que ingrediente existe
    ingredient = get_ingredient_by_id(conn, ingredient_id)
    if ingredient is None:
      logger.warning(f"Ingrediente no existe: {ingredient_id}")
      raise HTTPException(
        status_code=404,
        detail="Ingrediente no encontrado"
      )

    # Obtener datos
    total_waste = get_total_waste_by_ingredient(conn, ingredient_id)
    waste_cost = get_waste_cost_by_ingredient(conn, ingredient_id)

    logger.info(f"Análisis de merma obtenido para ingrediente: {ingredient_id}")

    return WasteIngredientAnalyticsResponse(
      ingredient_id=ingredient["id"],
      ingredient_name=ingredient["name"],
      unit=ingredient["unit"],
      total_quantity=total_waste,
      total_cost=waste_cost
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al obtener análisis: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener análisis de merma"
    )
  finally:
    conn.close()


def get_waste_analytics_by_date_range_service(data: DateRangeFilterRequest):
  """Obtiene análisis de merma en un rango de fechas"""
  conn = get_connection()

  try:
    # Obtener datos
    total_waste = get_total_waste_by_date_range(conn, data.start_date, data.end_date)
    waste_ratio_data = get_waste_ratio_by_date_range(conn, data.start_date, data.end_date)

    logger.info(f"Análisis de merma obtenido por rango de fechas")

    return WasteRatioResponse(
      waste_cost=waste_ratio_data["waste_cost"],
      consumption_cost=waste_ratio_data["consumption_cost"],
      total_cost=waste_ratio_data["total_cost"],
      waste_ratio=waste_ratio_data["waste_ratio"]
    )

  except Exception as e:
    logger.error(f"Error al obtener análisis: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener análisis de merma"
    )
  finally:
    conn.close()


def get_waste_reasons_summary_service():
  """Obtiene resumen de merma por motivo"""
  conn = get_connection()

  try:
    reasons = get_waste_reasons_summary(conn)

    logger.info(f"Resumen de motivos de merma obtenido")

    return [
      WasteReasonSummaryResponse(
        reason=item["reason"],
        count=item["count"],
        total_quantity=item["total_quantity"]
      )
      for item in reasons
    ]

  except Exception as e:
    logger.error(f"Error al obtener resumen: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener resumen de merma"
    )
  finally:
    conn.close()
