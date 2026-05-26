"""
API LAYER - Waste Logging
Rutas HTTP
"""

from fastapi import APIRouter, Depends
from shared.security.dependencies import get_current_user, get_current_admin
from modulos.merma.schemas import (
  WasteLogCreate, WasteLogResponse, WasteLogListResponse,
  WasteLogCreateResponse, WasteLogDeleteResponse,
  WasteAnalyticsResponse, WasteIngredientAnalyticsResponse,
  WasteRatioResponse, DateRangeFilterRequest, WasteReasonSummaryResponse
)
from modulos.merma.service import (
  create_waste_log_service, get_all_waste_logs_service, get_waste_log_service,
  get_waste_logs_by_ingredient_service, get_waste_logs_by_employee_service,
  get_waste_logs_by_turn_service, get_waste_logs_by_date_range_service,
  delete_waste_log_service, get_waste_analytics_by_ingredient_service,
  get_waste_analytics_by_date_range_service, get_waste_reasons_summary_service
)

router = APIRouter(prefix="/waste", tags=["waste"])


# ==========================================
# CRUD BÁSICO
# ==========================================

@router.post(
  "",
  response_model=WasteLogCreateResponse,
  status_code=201,
  summary="Registrar merma",
  description="Registra un nuevo evento de desperdicio"
)
def create_waste_log(
  data: WasteLogCreate,
  current_user = Depends(get_current_user)
):
  """
  Registra una nueva merma (desperdicio)

  - **ingredient_id**: ID del ingrediente (requerido)
  - **employee_id**: ID del empleado que registra (requerido)
  - **turn_id**: ID del turno (requerido)
  - **quantity**: Cantidad de merma (requerido)
  - **reason**: Motivo de la merma (opcional)
  """
  return create_waste_log_service(data)


@router.get(
  "",
  response_model=WasteLogListResponse,
  summary="Listar registros de merma",
  description="Obtiene lista de todos los registros de merma"
)
def list_waste_logs(current_user = Depends(get_current_user)):
  """Obtiene lista de todos los registros de merma"""
  return get_all_waste_logs_service()


@router.get(
  "/{waste_id}",
  response_model=WasteLogResponse,
  summary="Obtener registro de merma",
  description="Obtiene un registro específico de merma"
)
def get_waste_log(
  waste_id: int,
  current_user = Depends(get_current_user)
):
  """Obtiene los detalles de un registro de merma específico"""
  return get_waste_log_service(waste_id)


@router.delete(
  "/{waste_id}",
  response_model=WasteLogDeleteResponse,
  summary="Eliminar registro de merma",
  description="Solo administradores"
)
def delete_waste_log(
  waste_id: int,
  admin = Depends(get_current_admin)
):
  """Elimina un registro de merma"""
  return delete_waste_log_service(waste_id)


# ==========================================
# FILTROS
# ==========================================

@router.get(
  "/by-ingredient/{ingredient_id}",
  response_model=WasteLogListResponse,
  summary="Merma por ingrediente",
  description="Obtiene registros de merma de un ingrediente"
)
def get_waste_by_ingredient(
  ingredient_id: int,
  current_user = Depends(get_current_user)
):
  """Obtiene todos los registros de merma de un ingrediente específico"""
  return get_waste_logs_by_ingredient_service(ingredient_id)


@router.get(
  "/by-employee/{employee_id}",
  response_model=WasteLogListResponse,
  summary="Merma por empleado",
  description="Obtiene registros de merma de un empleado"
)
def get_waste_by_employee(
  employee_id: int,
  current_user = Depends(get_current_user)
):
  """Obtiene todos los registros de merma registrados por un empleado"""
  return get_waste_logs_by_employee_service(employee_id)


@router.get(
  "/by-turn/{turn_id}",
  response_model=WasteLogListResponse,
  summary="Merma por turno",
  description="Obtiene registros de merma de un turno"
)
def get_waste_by_turn(
  turn_id: int,
  current_user = Depends(get_current_user)
):
  """Obtiene todos los registros de merma de un turno específico"""
  return get_waste_logs_by_turn_service(turn_id)


@router.post(
  "/by-date-range",
  response_model=WasteLogListResponse,
  summary="Merma por rango de fechas",
  description="Obtiene registros de merma en un rango de fechas"
)
def get_waste_by_date_range(
  data: DateRangeFilterRequest,
  current_user = Depends(get_current_user)
):
  """
  Obtiene registros de merma en un rango de fechas

  - **start_date**: Fecha inicio (YYYY-MM-DD)
  - **end_date**: Fecha fin (YYYY-MM-DD)
  """
  return get_waste_logs_by_date_range_service(data)


# ==========================================
# ANALYTICS
# ==========================================

@router.get(
  "/analytics/ingredient/{ingredient_id}",
  response_model=WasteIngredientAnalyticsResponse,
  summary="Análisis de merma por ingrediente",
  description="Obtiene total y costo de merma de un ingrediente"
)
def get_waste_analytics_ingredient(
  ingredient_id: int,
  current_user = Depends(get_current_user)
):
  """Obtiene análisis de merma (cantidad y costo) de un ingrediente"""
  return get_waste_analytics_by_ingredient_service(ingredient_id)


@router.post(
  "/analytics/date-range",
  response_model=WasteRatioResponse,
  summary="Análisis de merma por fechas",
  description="Obtiene waste ratio en un rango de fechas"
)
def get_waste_analytics_date_range(
  data: DateRangeFilterRequest,
  current_user = Depends(get_current_user)
):
  """
  Obtiene análisis de merma en un rango de fechas

  - **start_date**: Fecha inicio (YYYY-MM-DD)
  - **end_date**: Fecha fin (YYYY-MM-DD)
  """
  return get_waste_analytics_by_date_range_service(data)


@router.get(
  "/analytics/reasons-summary",
  response_model=list[WasteReasonSummaryResponse],
  summary="Resumen de motivos de merma",
  description="Obtiene resumen de merma agrupado por motivo"
)
def get_waste_reasons_summary(current_user = Depends(get_current_user)):
  """Obtiene resumen de merma agrupado por motivo de desperdicio"""
  return get_waste_reasons_summary_service()
