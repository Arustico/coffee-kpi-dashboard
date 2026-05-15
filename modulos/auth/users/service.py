from fastapi import HTTPException
from shared.database import get_connection
from modulos.auth.schemas import (
    UserResponse, UserUpdate, UserListResponse,
    DeleteResponse, StatusUpdateResponse
    )
from modulos.auth.repository import (
    get_all_users, get_user_by_id, delete_user,
    desactivate_user, activate_user, update_user
    )

#-----------------
# SERVICES USERS
#-----------------

#------------------------------------------
# GET actual perfil del usuario
#------------------------------------------
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

#------------------------------------------
# GET lista de todos los usuarios
#------------------------------------------
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

		return UserListResponse(
				users=users,
				total=len(users)
		)

	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail="Error al obtener usuarios"
		)
	finally:
		conn.close()

#------------------------------------------
# GET datos de un usuario
#------------------------------------------
def get_user_service(user_id: int):
	"""Obtiene datos de un usuario específico"""
	conn = get_connection()

	try:
		user = get_user_by_id(conn, user_id)
		if user is None:
			raise HTTPException(
				status_code=404,
				detail="Usuario no encontrado"
			)

		return UserResponse(
			id=user["id"],
			email=user["email"],
			full_name=user["full_name"],
			rut=user["rut"],
			role_id=user["role_id"],
			active=bool(user["active"]),
			created_at=user["created_at"]
		)

	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail="Error al obtener usuario"
		)
	finally:
		conn.close()

#------------------------------------------
# DEL elimina a un usuario
#------------------------------------------
def delete_user_service(user_id: int, admin_user):
	"""Elimina un usuario"""
	# Validar que no se elimine a sí mismo
	if admin_user["id"] == user_id:
		raise HTTPException(
			status_code=400,
			detail="No puedes eliminar tu propia cuenta"
		)

	conn = get_connection()
	try:
		success = delete_user(conn, user_id)

		if not success:
			raise HTTPException(
				status_code=404,
				detail="Usuario no encontrado"
			)

		return DeleteResponse(
				message="Usuario eliminado exitosamente",
				id=user_id
		)

	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail="Error al eliminar usuario"
		)

	finally:
		conn.close()

#------------------------------------------
# UPDATE actualiza datos de usuario
#------------------------------------------
def update_user_service(user_id: int, data: UserUpdate, admin_user):
	"""Actualiza datos de un usuario"""
	conn = get_connection()

	try:
		# Actualizar usuario
		success = update_user(
			conn,
			user_id,
			email = data.email,
			rut = data.rut,
			full_name = data.full_name,
			role_id = data.role_id
		)

		if not success:
			raise HTTPException(
				status_code=404,
				detail="Usuario no encontrado"
			)

		# Obtener usuario actualizado
		user = get_user_by_id(conn, user_id)
		return UserResponse(
			id=user["id"],
			email=user["email"],
			full_name=user["full_name"],
			rut=user["rut"],
			role_id=user["role_id"],
			active=bool(user["active"]),
			created_at=user["created_at"]
		)

	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail="Error al actualizar usuario"
		)
	finally:
		conn.close()

def update_user_status_service(user_id: int, active: bool, admin_user):
	"""Activa o desactiva un usuario"""
	# Validar que no se desactive a sí mismo
	if admin_user["id"] == user_id and not active:
		raise HTTPException(
			status_code=400,
			detail="No puedes desactivar tu propia cuenta")
	conn = get_connection()
	try:
		if active:
			success = activate_user(conn, user_id)
		else:
			success = desactivate_user(conn, user_id)

		if not success:
			raise HTTPException(
				status_code=404,
				detail="Usuario no encontrado")

		action = "activado" if active else "desactivado"
		return StatusUpdateResponse(
			message=f"Usuario {action} exitosamente",
			id=user_id,
			active=active
		)

	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail="Error al cambiar estado del usuario"
		)
	finally:
		conn.close()
