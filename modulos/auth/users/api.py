
from fastapi import APIRouter, Depends
from shared.security.dependencies import get_current_user, get_current_admin

# Moduloes schemas
from modulos.auth.schemas import (
	UserResponse, UserUpdate, UserListResponse,UserStatusUpdate,
	DeleteResponse, StatusUpdateResponse)

# Modulos usuarios
from modulos.auth.users.service import (
	get_current_user_profile, get_all_users_service,
	get_user_service, delete_user_service,
	update_user_service, update_user_status_service)
#-----------------
# API USERS
#-----------------
router = APIRouter(tags=["users"])

@router.get(
	"/auth/me",
	response_model=UserResponse,
	summary="Obtener perfil del usuario actual",
	description="Retorna los datos del usuario autenticado"
)
def get_me(current_user = Depends(get_current_user)):
	"""
	Obtiene los datos del usuario actual. Requiere autenticación (token JWT)
	"""
	return get_current_user_profile(current_user)

@router.get(
	"/auth/users",
	response_model=UserListResponse,
	summary="Listar todos los usuarios",
	description="Solo administradores pueden ver la lista de usuarios"
)
def list_users(admin = Depends(get_current_admin)):
	"""
	Obtiene lista de todos los usuarios del sistema. Requiere permisos de administrador
	"""
	return get_all_users_service()

@router.get(
	"/auth/users/{user_id}",
	response_model=UserResponse,
	summary="Obtener usuario por ID",
	description="Solo administradores pueden ver datos de otros usuarios"
)
def get_user(user_id: int, admin = Depends(get_current_admin)):
	"""
	Obtiene los datos de un usuario específico. Requiere permisos de administrador
	"""
	return get_user_service(user_id)

@router.put(
	"/auth/users/{user_id}",
	response_model=UserResponse,
	summary="Actualizar usuario",
	description="Solo administradores pueden actualizar usuarios"
)
def update_user(user_id: int, data: UserUpdate,
								admin = Depends(get_current_admin)
								):
	"""
	Actualiza datos de un usuario:
	- **email**: Nuevo email (opcional)
	- **full_name**: Nuevo nombre (opcional)
	- **role_id**: Nuevo rol (opcional)

	Requiere permisos de administrador
	"""
	return update_user_service(user_id, data, admin)


@router.delete(
	"/auth/users/{user_id}",
	response_model=DeleteResponse,
	summary="Eliminar usuario",
	description="Solo administradores pueden eliminar usuarios"
)
def delete_user(user_id: int, admin = Depends(get_current_admin)):
	"""
	Elimina un usuario del sistema - No puedes eliminar tu propia cuenta.
	Requiere permisos de administrador
	"""
	return delete_user_service(user_id, admin)


@router.patch(
	"/auth/users/{user_id}/status",
	response_model=StatusUpdateResponse,
	summary="Cambiar estado de usuario",
	description="Activar o desactivar un usuario"
)
def update_user_status(	user_id: int,
												data: UserStatusUpdate,
												admin = Depends(get_current_admin)
											):
	"""
	Activa o desactiva un usuario. **active**: True para activar, False para desactivar
	Requiere permisos de administrador
	"""
	return update_user_status_service(user_id, data.active, admin)



