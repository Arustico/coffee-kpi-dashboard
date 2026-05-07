
from fastapi import HTTPException

def user_exists(conn, email: str) -> bool:
	"""Verifica si un usuario ya existe por email"""
	row = conn.execute("""
		SELECT id FROM "User" WHERE email = ?
	""", (email,)).fetchone()
	return row is not None

def create_user(conn, email: str, hashed_password: str, full_name: str, role_id: int) -> int:
	"""Crea un nuevo usuario en la BD"""
	cursor = conn.execute("""
		INSERT INTO "User" (email, hashed_password, full_name, role_id)
		VALUES (?, ?, ?, ?)
	""", (email, hashed_password, full_name, role_id))
	conn.commit()
	return cursor.lastrowid

def get_user_by_email(conn, email: str):
	"""Obtiene usuario por email"""
	row = conn.execute("""
		SELECT id, email, hashed_password, full_name, role_id, active
		FROM "User" WHERE email = ?
	""", (email,)).fetchone()
	return row

def get_user_by_id(conn, user_id: int):
	"""Obtiene usuario por ID"""
	row = conn.execute("""
		SELECT id, email, full_name, role_id, active
		FROM "User" WHERE id = ?
	""", (user_id,)).fetchone()
	return row

def update_last_login(conn, user_id: int):
	"""Actualiza fecha de último login"""
	conn.execute("""
		UPDATE "User" SET updated_at = CURRENT_TIMESTAMP
		WHERE id = ?
	""", (user_id,))
	conn.commit()
