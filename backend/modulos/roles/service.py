"""
SERVICE LAYER - Roles & Permissions
Lógica de negocio, validaciones, transacciones
"""

from fastapi import HTTPException
from shared.database import get_connection
from modulos.roles.repository import (
  create_permission, get_permission_by_id, get_permissions_by_role,
  get_all_permissions, permission_exists, delete_permission,
  delete_permissions_by_role, get_user_permissions, user_has_permission,
  get_role_by_id, get_all_roles, role_exists
)
from modulos.roles.schemas import (
  RolePermissionCreate, PermissionResponse, RoleWithPermissionsResponse,
  UserPermissionsResponse, PermissionCheckResponse
)
from modulos.auth.repository import get_user_by_id
import logging

logger = logging.getLogger(__name__)


def create_permission_service(data: RolePermissionCreate, admin_user):
  """Crea un nuevo permiso para un rol"""
  conn = get_connection()

  try:
    conn.execute("BEGIN")
    logger.info(f"Creando permiso: {data.module}:{data.action} para rol {data.role_id}")

    # Validar que rol existe
    if not role_exists(conn, data.role_id):
      logger.warning(f"Rol no existe: {data.role_id}")
      conn.rollback()
      raise HTTPException(
        status_code=404,
        detail="Rol no encontrado"
      )

    # Validar que permiso no existe
    if permission_exists(conn, data.role_id, data.module, data.action):
      logger.warning(f"Permiso duplicado: {data.module}:{data.action}")
      conn.rollback()
      raise HTTPException(
        status_code=400,
        detail="Permiso ya existe para este rol"
      )

    # Crear permiso
    permission_id = create_permission(
      conn,
      role_id=data.role_id,
      module=data.module,
      action=data.action
    )

    conn.commit()
    logger.info(f"Permiso creado: {permission_id}")

    return PermissionResponse(
      id=permission_id,
      role_id=data.role_id,
      module=data.module,
      action=data.action
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al crear permiso: {str(e)}")
    try:
      conn.rollback()
    except:
      pass
    raise HTTPException(
      status_code=500,
      detail="Error al crear permiso"
    )
  finally:
    conn.close()


def get_role_with_permissions_service(role_id: int):
  """Obtiene un rol con sus permisos"""
  conn = get_connection()

  try:
    # Obtener rol
    role = get_role_by_id(conn, role_id)
    if role is None:
      logger.warning(f"Rol no encontrado: {role_id}")
      raise HTTPException(
        status_code=404,
        detail="Rol no encontrado"
      )

    # Obtener permisos
    permissions_rows = get_permissions_by_role(conn, role_id)

    permissions = [
      PermissionResponse(
        id=p["id"],
        role_id=p["role_id"],
        module=p["module"],
        action=p["action"]
      )
      for p in permissions_rows
    ]

    logger.info(f"Rol con permisos obtenido: {role_id}")

    return RoleWithPermissionsResponse(
      id=role["id"],
      name=role["name"],
      permissions=permissions
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al obtener rol: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener rol"
    )
  finally:
    conn.close()


def get_all_roles_with_permissions_service():
  """Obtiene todos los roles con sus permisos"""
  conn = get_connection()

  try:
    roles = get_all_roles(conn)

    roles_response = []
    for role in roles:
      permissions_rows = get_permissions_by_role(conn, role["id"])
      permissions = [
        PermissionResponse(
          id=p["id"],
          role_id=p["role_id"],
          module=p["module"],
          action=p["action"]
        )
        for p in permissions_rows
      ]

      roles_response.append(
        RoleWithPermissionsResponse(
          id=role["id"],
          name=role["name"],
          permissions=permissions
        )
      )

    logger.info(f"Roles con permisos obtenidos: {len(roles_response)}")

    return roles_response

  except Exception as e:
    logger.error(f"Error al obtener roles: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener roles"
    )
  finally:
    conn.close()


def get_user_permissions_service(user_id: int):
  """Obtiene los permisos del usuario"""
  conn = get_connection()

  try:
    # Obtener usuario
    user = get_user_by_id(conn, user_id)
    if user is None:
      logger.warning(f"Usuario no encontrado: {user_id}")
      raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
      )

    # Obtener rol
    role = get_role_by_id(conn, user["role_id"])

    # Obtener permisos
    permissions_rows = get_user_permissions(conn, user_id)

    permissions = [
      f"{p['module']}:{p['action']}"
      for p in permissions_rows
    ]

    logger.info(f"Permisos del usuario obtenidos: {user_id}")

    return UserPermissionsResponse(
      user_id=user["id"],
      email=user["email"],
      role=role["name"] if role else "Unknown",
      permissions=permissions
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al obtener permisos: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener permisos"
    )
  finally:
    conn.close()


def check_user_permission_service(user_id: int, module: str, action: str):
  """Verifica si usuario tiene permiso específico"""
  conn = get_connection()

  try:
    has_permission = user_has_permission(conn, user_id, module, action)

    logger.info(f"Verificación de permiso: usuario {user_id}, {module}:{action} = {has_permission}")

    return PermissionCheckResponse(
      has_permission=has_permission,
      message="Usuario tiene permiso para esta acción" if has_permission else "Usuario NO tiene permiso"
    )

  except Exception as e:
    logger.error(f"Error al verificar permiso: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al verificar permiso"
    )
  finally:
    conn.close()


def delete_permission_service(permission_id: int, admin_user):
  """Elimina un permiso"""
  conn = get_connection()

  try:
    conn.execute("BEGIN")

    # Verificar que existe
    permission = get_permission_by_id(conn, permission_id)
    if permission is None:
      conn.rollback()
      logger.warning(f"Permiso no encontrado: {permission_id}")
      raise HTTPException(
        status_code=404,
        detail="Permiso no encontrado"
      )

    # Eliminar
    delete_permission(conn, permission_id)

    conn.commit()
    logger.info(f"Permiso eliminado: {permission_id}")

    return {
      "message": "Permiso eliminado exitosamente",
      "permission_id": permission_id
    }

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al eliminar permiso: {str(e)}")
    try:
      conn.rollback()
    except:
      pass
    raise HTTPException(
      status_code=500,
      detail="Error al eliminar permiso"
    )
  finally:
    conn.close()
