"""
API LAYER - Roles & Permissions
Rutas HTTP
"""

from fastapi import APIRouter, Depends
from shared.security.dependencies import get_current_user, get_current_admin
from modulos.roles.schemas import (
  RolePermissionCreate, PermissionResponse, RoleWithPermissionsResponse,
  UserPermissionsResponse, PermissionCheckResponse
)
from modulos.roles.service import (
  create_permission_service, get_role_with_permissions_service,
  get_all_roles_with_permissions_service, get_user_permissions_service,
  check_user_permission_service, delete_permission_service
)

router = APIRouter(prefix="/roles", tags=["roles"])


@router.post(
  "/permissions",
  response_model=PermissionResponse,
  status_code=201,
  summary="Crear permiso",
  description="Solo administradores"
)
def create_permission(
  data: RolePermissionCreate,
  admin = Depends(get_current_admin)
):
  """
  Crea un nuevo permiso para un rol

  - **role_id**: ID del rol (requerido)
  - **module**: Nombre del módulo (requerido)
  - **action**: Acción permitida (requerido)
  """
  return create_permission_service(data, admin)


@router.get(
  "/{role_id}/permissions",
  response_model=RoleWithPermissionsResponse,
  summary="Obtener rol con permisos",
  description="Obtiene un rol y sus permisos"
)
def get_role_permissions(
  role_id: int,
  current_user = Depends(get_current_user)
):
  """Obtiene un rol con todos sus permisos asociados"""
  return get_role_with_permissions_service(role_id)


@router.get(
  "",
  response_model=list[RoleWithPermissionsResponse],
  summary="Listar roles con permisos",
  description="Obtiene todos los roles con sus permisos"
)
def list_roles(current_user = Depends(get_current_user)):
  """Obtiene lista de todos los roles con sus permisos"""
  return get_all_roles_with_permissions_service()


@router.get(
  "/current/permissions",
  response_model=UserPermissionsResponse,
  summary="Mis permisos",
  description="Obtiene los permisos del usuario actual"
)
def get_my_permissions(current_user = Depends(get_current_user)):
  """Obtiene los permisos del usuario autenticado"""
  return get_user_permissions_service(current_user["id"])


@router.post(
  "/check",
  response_model=PermissionCheckResponse,
  summary="Verificar permiso",
  description="Verifica si el usuario tiene un permiso específico"
)
def check_permission(
  module: str,
  action: str,
  current_user = Depends(get_current_user)
):
  """
  Verifica si el usuario tiene un permiso específico

  - **module**: Nombre del módulo
  - **action**: Acción a verificar
  """
  return check_user_permission_service(current_user["id"], module, action)


@router.delete(
  "/permissions/{permission_id}",
  summary="Eliminar permiso",
  description="Solo administradores"
)
def delete_permission(
  permission_id: int,
  admin = Depends(get_current_admin)
):
  """Elimina un permiso específico"""
  return delete_permission_service(permission_id, admin)
