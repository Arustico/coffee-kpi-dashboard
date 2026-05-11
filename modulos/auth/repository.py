
from fastapi import HTTPException

#-----------------------------------
# Chequeo existencia de usuario
#-----------------------------------
def user_exists(conn, email: str) -> bool:
	"""Verifica si un usuario ya existe por email"""
	row = conn.execute("""
		SELECT id FROM "User" WHERE email = ?
	""", (email,)).fetchone()
	return row is not None

#-----------------------------------
# POST Creación de usuario
#-----------------------------------
def create_user(conn, email: str, hashed_password: str, full_name: str, role_id: int) -> int:
	"""Crea un nuevo usuario en la BD"""
	cursor = conn.execute("""
		INSERT INTO "User" (email, hashed_password, full_name, role_id)
		VALUES (?, ?, ?, ?)
	""", (email, hashed_password, full_name, role_id))
	conn.commit()
	return cursor.lastrowid

#-----------------------------------
# GET Consulta de usuario por mail
#-----------------------------------
def get_user_by_email(conn, email: str):
	"""Obtiene usuario por email"""
	row = conn.execute("""
		SELECT id, email, hashed_password, full_name, role_id, active
		FROM "User" WHERE email = ?
	""", (email,)).fetchone()
	return row

#-----------------------------------
# GET Consulta de usuario por id
#-----------------------------------
def get_user_by_id(conn, user_id: int):
	"""Obtiene usuario por ID"""
	row = conn.execute("""
		SELECT id, email, full_name, role_id, active
		FROM "User" WHERE id = ?
	""", (user_id,)).fetchone()
	return row

#-----------------------------------
# POST Actuliza fecha de login de usuario
#-----------------------------------
def update_last_login(conn, user_id: int):
	"""Actualiza fecha de último login"""
	conn.execute("""
		UPDATE "User" SET updated_at = CURRENT_TIMESTAMP
		WHERE id = ?
	""", (user_id,))
	conn.commit()

#-----------------------------------
# GET de todos los usuarios
#-----------------------------------
def get_all_users(conn):
	""" Obtiene lista de todos los usuarios """
	rows = conn.execute("""
		SELECT id, email, full_name, role_id, active, created_at, updated_at
		FROM "User"
		ORDER BY created_at DESC
	""").fetchall()
	return rows

#-----------------------------------
# DELETE elimina un usuario
#-----------------------------------
def delete_user(conn, user_id: int) -> bool:
	""" Elimina un usuario de forma permanente.
	Returns: True si fue eliminado, False si no existe
	"""
	try:
		# Verificar que existe
		user = get_user_by_id(conn, user_id)
		if user is None:
			return False
		# Eliminar
		conn.execute("""
			DELETE FROM "User" WHERE id = ?
		""", (user_id,))
		conn.commit()
		return True
	except Exception as e:
		conn.rollback()
		raise

#-----------------------------------
# DESACTIVA un usuario
#-----------------------------------

def desactivate_user(conn, user_id: int) -> bool:
	"""
	Desactiva un usuario. Es mejor que eliminar permanentemente
	Returns: True si fue desactivado, False si no existe
	"""
	try:
		user = get_user_by_id(conn, user_id)
		if user is None:
			return False

		conn.execute("""
			UPDATE "User" SET active = 0, updated_at = CURRENT_TIMESTAMP
			WHERE id = ?
		""", (user_id,))

		conn.commit()
		return True

	except Exception as e:
		conn.rollback()
		raise


def activate_user(conn, user_id: int) -> bool:
	"""
	Activa un usuario desactivado.
	Returns:True si fue activado, False si no existe
	"""
	try:
		user = get_user_by_id(conn, user_id)
		if user is None:
			logger.warning(f"Intento de activar usuario inexistente: {user_id}")
			return False

		conn.execute("""
			UPDATE "User" SET active = 1, updated_at = CURRENT_TIMESTAMP
			WHERE id = ?
		""", (user_id,))

		conn.commit()
		return True

	except Exception as e:
		conn.rollback()
		raise
