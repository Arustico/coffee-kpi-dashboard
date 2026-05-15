from fastapi import APIRouter, Depends
from shared.security.dependencies import get_current_admin

from modulos.auth.schemas import (
	EmployeeCreate, EmployeeUpdate, EmployeeResponse,
	EmployeeListResponse, DeleteResponse, StatusUpdateResponse
  )

from modulos.employees.service import (
	create_employee_service, get_all_employees_service,
	get_active_employees_service, get_employee_service,
	update_employee_service, delete_employee_service,
	update_employee_status_service
	)

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post(
	"",
	response_model=EmployeeResponse,
	status_code=201,
	summary="Crear nuevo empleado",
	description="Solo administradores pueden crear empleados"
)
def create_employee(data: EmployeeCreate, admin = Depends(get_current_admin)):
	"""
	Crea un nuevo empleado

	- **full_name**: Nombre completo (obligatorio)
	- **rut**: RUT/Documento (obligatorio, único)
	- **role_id**: ID del rol (obligatorio)
	- **user_id**: ID del usuario del sistema (opcional)
	- **phone**: Teléfono (opcional)
	- **address**: Dirección (opcional)
	"""
	return create_employee_service(data, admin)


@router.get(
	"",
	response_model=EmployeeListResponse,
	summary="Listar todos los empleados",
	description="Solo administradores"
)
def list_employees(admin = Depends(get_current_admin)):
	"""Obtiene lista de todos los empleados"""
	return get_all_employees_service()


@router.get(
	"/active",
	response_model=EmployeeListResponse,
	summary="Listar empleados activos",
	description="Solo administradores"
)
def list_active_employees(admin = Depends(get_current_admin)):
	"""Obtiene lista de empleados activos"""
	return get_active_employees_service()


@router.get(
	"/{employee_id}",
	response_model=EmployeeResponse,
	summary="Obtener empleado por ID",
	description="Solo administradores"
)
def get_employee(employee_id: int, admin = Depends(get_current_admin)):
	"""Obtiene los datos de un empleado específico"""
	return get_employee_service(employee_id)


@router.put(
	"/{employee_id}",
	response_model=EmployeeResponse,
	summary="Actualizar empleado",
	description="Solo administradores"
)
def update_employee(employee_id: int,
										data: EmployeeUpdate,
										admin = Depends(get_current_admin)):
	"""
	Actualiza datos de un empleado
- **full_name**: Nuevo nombre (opcional)
- **rut**: Nuevo RUT (opcional)
- **role_id**: Nuevo rol (opcional)
- **phone**: Nuevo teléfono (opcional)
- **address**: Nueva dirección (opcional)
    """
	return update_employee_service(employee_id, data, admin)


@router.delete(
	"/{employee_id}",
	response_model=DeleteResponse,
	summary="Eliminar empleado",
	description="Solo administradores"
)
def delete_employee(employee_id: int, admin = Depends(get_current_admin)):
	"""Elimina un empleado del sistema"""
	return delete_employee_service(employee_id, admin)


@router.patch(
	"/{employee_id}/status",
	response_model=StatusUpdateResponse,
	summary="Cambiar estado de empleado",
	description="Activar o desactivar"
)
def update_employee_status( employee_id: int,
														active: bool,
														admin = Depends(get_current_admin)):
	""" Activa o desactiva un empleado
	- **active**: True para activar, False para desactivar
	"""
	return update_employee_status_service(employee_id, active, admin)
