
from fastapi import HTTPException
"""
REPOSITORY LAYER - Solo acceso a datos SQL
Sin lógica de negocio, sin transacciones, sin commits/rollbacks
"""

from typing import Optional
import logging

logger = logging.getLogger(__name__)

# ==========================================
# USER REPOSITORY - Funciones de acceso SQL
# ==========================================

def user_exists(conn, email: str) -> bool:
	"""Verifica si un usuario existe por email"""
	row = conn.execute("""
		SELECT id FROM "User" WHERE email = ?
	""", (email,)).fetchone()
	return row is not None


def user_rut_exists(conn, rut: str) -> bool:
	"""Verifica si un RUT existe en usuarios"""
	row = conn.execute("""
		SELECT id FROM "User" WHERE rut = ?
	""", (rut,)).fetchone()
	return row is not None


def create_user(
	conn,
	email: str,
	hashed_password: str,
	full_name: str,
	role_id: int,
	rut: Optional[str] = None) -> int:
	"""
	Inserta un nuevo usuario en BD. Returns: ID del usuario creado
	"""
	cursor = conn.execute("""
		INSERT INTO "User" (email, hashed_password, full_name, rut, role_id)
		VALUES (?, ?, ?, ?, ?)
	""", (email, hashed_password, full_name, rut, role_id))
	return cursor.lastrowid


def get_user_by_email(conn, email: str):
	"""Obtiene usuario por email (con contraseña hasheada)"""
	row = conn.execute("""
		SELECT id, email, hashed_password, full_name, rut, role_id, active, created_at
		FROM "User" WHERE email = ?
	""", (email,)).fetchone()
	return row


def get_user_by_id(conn, user_id: int):
	"""Obtiene usuario por ID (sin contraseña)"""
	row = conn.execute("""
		SELECT id, email, full_name, rut, role_id, active, created_at
		FROM "User" WHERE id = ?
	""", (user_id,)).fetchone()
	return row


def get_all_users(conn):
	"""Obtiene lista de todos los usuarios"""
	rows = conn.execute("""
		SELECT id, email, full_name, rut, role_id, active, created_at, updated_at
		FROM "User"
		ORDER BY created_at DESC
	""").fetchall()
	return rows


def update_user_email(conn, user_id: int, email: str):
	"""Actualiza email del usuario"""
	conn.execute("""
		UPDATE "User" SET email = ?, updated_at = CURRENT_TIMESTAMP
		WHERE id = ?
	""", (email, user_id))


def update_user_rut(conn, user_id: int, rut: str):
	"""Actualiza RUT del usuario"""
	conn.execute("""
		UPDATE "User" SET rut = ?, updated_at = CURRENT_TIMESTAMP
		WHERE id = ?
	""", (rut, user_id))


def update_user_full_name(conn, user_id: int, full_name: str):
	"""Actualiza nombre del usuario"""
	conn.execute("""
		UPDATE "User" SET full_name = ?, updated_at = CURRENT_TIMESTAMP
		WHERE id = ?
	""", (full_name, user_id))


def update_user_role_id(conn, user_id: int, role_id: int):
	"""Actualiza rol del usuario"""
	conn.execute("""
		UPDATE "User" SET role_id = ?, updated_at = CURRENT_TIMESTAMP
		WHERE id = ?
	""", (role_id, user_id))


def update_user_last_login(conn, user_id: int):
	"""Actualiza timestamp de último login"""
	conn.execute("""
		UPDATE "User" SET updated_at = CURRENT_TIMESTAMP
		WHERE id = ?
	""", (user_id,))


def deactivate_user(conn, user_id: int):
	"""Desactiva un usuario (soft delete)"""
	conn.execute("""
		UPDATE "User" SET active = 0, updated_at = CURRENT_TIMESTAMP
		WHERE id = ?
	""", (user_id,))


def activate_user(conn, user_id: int):
	"""Activa un usuario"""
	conn.execute("""
		UPDATE "User" SET active = 1, updated_at = CURRENT_TIMESTAMP
		WHERE id = ?
	""", (user_id,))


def delete_user(conn, user_id: int):
	"""Elimina un usuario de forma permanente (hard delete)"""
	conn.execute("""
		DELETE FROM "User" WHERE id = ?
	""", (user_id,))


def update_last_login(conn, user_id: int):
	"""Actualiza el último login del usuario"""
	conn.execute("""
		UPDATE "User" SET updated_at = CURRENT_TIMESTAMP
		WHERE id = ?
	""", (user_id,))


# ==========================================
# EMPLOYEE REPOSITORY - Funciones de acceso SQL
# ==========================================

def employee_rut_exists(conn, rut: str) -> bool:
	"""Verifica si un RUT existe en empleados"""
	row = conn.execute("""
		SELECT id FROM "Employee" WHERE rut = ?
	""", (rut,)).fetchone()
	return row is not None


def create_employee(
	conn,
	full_name: str,
	rut: str,
	role_id: int,
	user_id: Optional[int] = None,
	phone: Optional[str] = None,
	address: Optional[str] = None) -> int:
	"""
	Inserta un nuevo empleado en BD. Returns: ID del empleado creado
	"""
	cursor = conn.execute("""
		INSERT INTO "Employee" (full_name, rut, role_id, user_id, phone, address)
		VALUES (?, ?, ?, ?, ?, ?)
	""", (full_name, rut, role_id, user_id, phone, address))
	return cursor.lastrowid


def get_employee_by_id(conn, employee_id: int):
	"""Obtiene empleado por ID"""
	row = conn.execute("""
		SELECT id, full_name, rut, role_id, user_id, active, phone, address, hire_date, created_at
		FROM "Employee" WHERE id = ?
	""", (employee_id,)).fetchone()
	return row


def get_employee_by_rut(conn, rut: str):
	"""Obtiene empleado por RUT"""
	row = conn.execute("""
		SELECT id, full_name, rut, role_id, user_id, active, phone, address, hire_date, created_at
		FROM "Employee" WHERE rut = ?
	""", (rut,)).fetchone()
	return row


def get_all_employees(conn):
	"""Obtiene lista de todos los empleados"""
	rows = conn.execute("""
		SELECT id, full_name, rut, role_id, user_id, active, phone, address, hire_date, created_at
		FROM "Employee"
		ORDER BY created_at DESC
	""").fetchall()
	return rows


def get_active_employees(conn):
	"""Obtiene lista de empleados activos"""
	rows = conn.execute("""
		SELECT id, full_name, rut, role_id, user_id, active, phone, address, hire_date, created_at
		FROM "Employee"
		WHERE active = 1
		ORDER BY full_name
	""").fetchall()
	return rows


def update_employee_full_name(conn, employee_id: int, full_name: str):
	"""Actualiza nombre del empleado"""
	conn.execute("""
		UPDATE "Employee" SET full_name = ?, updated_at = CURRENT_TIMESTAMP
		WHERE id = ?
	""", (full_name, employee_id))


def update_employee_rut(conn, employee_id: int, rut: str):
	"""Actualiza RUT del empleado"""
	conn.execute("""
		UPDATE "Employee" SET rut = ?, updated_at = CURRENT_TIMESTAMP
		WHERE id = ?
	""", (rut, employee_id))


def update_employee_role_id(conn, employee_id: int, role_id: int):
	"""Actualiza rol del empleado"""
	conn.execute("""
		UPDATE "Employee" SET role_id = ?, updated_at = CURRENT_TIMESTAMP
		WHERE id = ?
	""", (role_id, employee_id))


def update_employee_phone(conn, employee_id: int, phone: str):
	"""Actualiza teléfono del empleado"""
	conn.execute("""
		UPDATE "Employee" SET phone = ?, updated_at = CURRENT_TIMESTAMP
		WHERE id = ?
	""", (phone, employee_id))


def update_employee_address(conn, employee_id: int, address: str):
	"""Actualiza dirección del empleado"""
	conn.execute("""
		UPDATE "Employee" SET address = ?, updated_at = CURRENT_TIMESTAMP
		WHERE id = ?
	""", (address, employee_id))


def deactivate_employee(conn, employee_id: int):
	"""Desactiva un empleado (soft delete)"""
	conn.execute("""
		UPDATE "Employee" SET active = 0, updated_at = CURRENT_TIMESTAMP
		WHERE id = ?
	""", (employee_id,))


def activate_employee(conn, employee_id: int):
	"""Activa un empleado"""
	conn.execute("""
		UPDATE "Employee" SET active = 1, updated_at = CURRENT_TIMESTAMP
		WHERE id = ?
	""", (employee_id,))

def delete_employee(conn, employee_id: int):
	"""Elimina un empleado de forma permanente (hard delete)"""
	conn.execute("""
		DELETE FROM "Employee" WHERE id = ?
	""", (employee_id,))

