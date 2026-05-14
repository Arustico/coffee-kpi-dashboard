
from fastapi import HTTPException

#-----------------------------------
# Chequeo existencia de usuario
#-----------------------------------
def user_exists(conn, email: str) -> bool:
	"""Verifica si un usuario ya existe por email"""
	row = conn.execute("""
		SELECT id FROM "User" WHERE email = ?
	""", (email,)).fetchone()
	exists = row is not None
	return exists

# Existencia del rut
def user_rut_exists(conn, rut: str) -> bool:
	"""Verifica si un RUT ya está registrado en usuarios"""
	row = conn.execute("""
		SELECT id FROM "User" WHERE rut = ?
	""", (rut,)).fetchone()
	exists = row is not None
	return exists

#-----------------------------------
# POST Creación de usuario
#-----------------------------------
def create_user(conn, email: str, hashed_password: str,
								full_name: str, role_id: int, rut: str = None
								) -> int:
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
	"""Obtiene usuario por email con contraseña (hasheada)"""
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

#-----------------------------------
# ACTUALIZA un usuario
#-----------------------------------

def update_user(conn, user_id: int, email: str = None,
								rut: str = None, full_name: str = None,
								role_id: int = None
							) -> bool:
	"""Actualiza datos de un usuario"""
	try:
		user = get_user_by_id(conn, user_id)
		if user is None:
			logger.warning(f"Intento de actualizar usuario inexistente: {user_id}")
			return False

		updates = []
		params = []

		if email is not None:
			updates.append("email = ?")
			params.append(email)

		if rut is not None:
			updates.append("rut = ?")
			params.append(rut)

		if full_name is not None:
			updates.append("full_name = ?")
			params.append(full_name)

		if role_id is not None:
			updates.append("role_id = ?")
			params.append(role_id)

		if not updates:
			return True

		updates.append("updated_at = CURRENT_TIMESTAMP")
		params.append(user_id)

		query = f"""
			UPDATE "User" SET {', '.join(updates)}
			WHERE id = ?
		"""
		conn.execute(query, params)
		conn.commit()
		logger.info(f"Usuario actualizado: {user_id}")
		return True

	except Exception as e:
		conn.rollback()
		raise
