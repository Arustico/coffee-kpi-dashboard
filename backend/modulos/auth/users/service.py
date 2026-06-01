from fastapi import HTTPException
from shared.database import get_connection
from modulos.auth.schemas import (
  UserResponse, UserUpdate, UserListResponse,
  DeleteResponse, StatusUpdateResponse
)
from modulos.auth.repository import (
  get_all_users, get_user_by_id, delete_user,
  desactivate_user, activate_user,
  update_user_email, update_user_rut, update_user_full_name, update_user_role_id
)
import logging

logger = logging.getLogger(__name__)

def get_current_user_profile(current_user):
  """Obtiene los datos del usuario actual autenticado"""
  return UserResponse(
    id=current_user["id"],
    email=current_user["email"],
    full_name=current_user["full_name"],
    rut=current_user["rut"],
    role_id=current_user["role_id"],
    active=bool(current_user["active"]),
    created_at=current_user.get("created_at")
  )



def get_all_users_service():
  """Obtiene lista de todos los usuarios"""
  conn = get_connection()
  try:
    rows = get_all_users(conn)
    users = [
      UserResponse(
        id=row["id"],
        email=row["email"],
        full_name=row["full_name"],
        rut=row["rut"],
        role_id=row["role_id"],
        active=bool(row["active"]),
        created_at=row["created_at"]
      )
      for row in rows
    ]

    logger.info(f"Usuarios listados: {len(users)}")
    return UserListResponse(
      users=users,
      total=len(users))

  except Exception as e:
    logger.error(f"Error al obtener usuarios: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener usuarios"
    )
  finally:
    conn.close()


def get_user_service(user_id: int):
  """Obtiene datos de un usuario específico"""
  conn = get_connection()

  try:
    user = get_user_by_id(conn, user_id)

    if user is None:
      logger.warning(f"Usuario no encontrado: {user_id}")
      raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado")

    return UserResponse(
      id=user["id"],
      email=user["email"],
      full_name=user["full_name"],
      rut=user["rut"],
      role_id=user["role_id"],
      active=bool(user["active"]),
      created_at=user["created_at"]
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al obtener usuario {user_id}: {str(e)}")
    raise HTTPException(
      status_code=500,
      detail="Error al obtener usuario"
    )
  finally:
    conn.close()


def delete_user_service(user_id: int, admin_user):
  """Elimina un usuario"""
  if admin_user["id"] == user_id:
    logger.warning(f"Admin intentó eliminarse a sí mismo (tas reloco che): {user_id}")
    raise HTTPException(
      status_code=400,
      detail="No puedes eliminar tu propia cuenta")

  conn = get_connection()
  try:
    conn.execute("BEGIN")
    # Verificar que existe
    user = get_user_by_id(conn, user_id)
    if user is None:
      conn.rollback()
      raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
      )

    # Eliminar
    delete_user(conn, user_id)
    conn.commit()

    logger.info(f"Usuario eliminado: {user_id} por admin: {admin_user['id']}")

    return DeleteResponse(
      message="Usuario eliminado exitosamente",
      id=user_id
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al eliminar usuario: {str(e)}")
    try:
      conn.rollback()
    except:
      pass
    raise HTTPException(
      status_code=500,
      detail="Error al eliminar usuario"
    )
  finally:
    conn.close()


def update_user_service(user_id: int, data: UserUpdate, admin_user):
  """Actualiza datos de un usuario"""
  conn = get_connection()

  try:
    conn.execute("BEGIN")

    # Verificar que existe
    user = get_user_by_id(conn, user_id)
    if user is None:
      conn.rollback()
      raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
      )

    # Actualizar campos
    if data.email is not None:
      update_user_email(conn, user_id, data.email)

    if data.rut is not None:
      update_user_rut(conn, user_id, data.rut)

    if data.full_name is not None:
      update_user_full_name(conn, user_id, data.full_name)

    if data.role_id is not None:
      update_user_role_id(conn, user_id, data.role_id)

    # Obtener usuario actualizado
    user = get_user_by_id(conn, user_id)
    conn.commit()

    logger.info(f"Usuario actualizado: {user_id} por admin: {admin_user['id']}")

    return UserResponse(
      id=user["id"],
      email=user["email"],
      full_name=user["full_name"],
      rut=user["rut"],
      role_id=user["role_id"],
      active=bool(user["active"]),
      created_at=user["created_at"]
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al actualizar usuario: {str(e)}")
    try:
      conn.rollback()
    except:
      pass
    raise HTTPException(
      status_code=500,
      detail="Error al actualizar usuario"
    )
  finally:
    conn.close()


def update_user_status_service(user_id: int, active: bool, admin_user):
  """Activa o desactiva un usuario"""

  if admin_user["id"] == user_id and not active:
    logger.warning(f"Admin intentó desactivarse a sí mismo: {user_id}")
    raise HTTPException(
      status_code=400,
      detail="No puedes desactivar tu propia cuenta"
    )

  conn = get_connection()

  try:
    conn.execute("BEGIN")

    # Verificar que existe
    user = get_user_by_id(conn, user_id)
    if user is None:
      conn.rollback()
      raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
      )

    # Cambiar estado
    if active:
      activate_user(conn, user_id)
    else:
      desactivate_user(conn, user_id)

    conn.commit()

    action = "activado" if active else "desactivado"
    logger.info(f"Usuario {action}: {user_id} por admin: {admin_user['id']}")

    return StatusUpdateResponse(
      message=f"Usuario {action} exitosamente",
      id=user_id,
      active=active
    )

  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error al cambiar estado: {str(e)}")
    try:
      conn.rollback()
    except:
      pass
    raise HTTPException(
      status_code=500,
      detail="Error al cambiar estado del usuario"
    )
  finally:
    conn.close()
