
from fastapi import HTTPException

#---------------------------------
# REPOSITORY EMPLOYEES
#---------------------------------

def employee_rut_exists(conn, rut: str) -> bool:
	"""Verifica si un RUT ya está registrado en empleados"""
	row = conn.execute("""
			SELECT id FROM "Employee" WHERE rut = ?
	""", (rut,)).fetchone()
	exists = row is not None
	if exists:
	return exists


def create_employee(conn,
										full_name: str, rut: str,
										role_id: int, user_id: int = None,
										phone: str = None, address: str = None) -> int:
	"""
	Crea un nuevo empleado. Returns: ID del empleado creado
	"""
	try:
		cursor = conn.execute("""
			INSERT INTO "Employee" (full_name, rut, role_id, user_id, phone, address)
			VALUES (?, ?, ?, ?, ?, ?)
		""", (full_name, rut, role_id, user_id, phone, address))

		conn.commit()
		employee_id = cursor.lastrowid
		return employee_id

	except Exception as e:
		conn.rollback()
		raise


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


def update_employee(conn,
										employee_id: int, full_name: str = None,
										rut: str = None, role_id: int = None,
										phone: str = None, address: str = None) -> bool:
	"""Actualiza datos de un empleado"""
	try:
		employee = get_employee_by_id(conn, employee_id)
		if employee is None:
			return False

		updates = []
		params = []

		if full_name is not None:
			updates.append("full_name = ?")
			params.append(full_name)

		if rut is not None:
			updates.append("rut = ?")
			params.append(rut)

		if role_id is not None:
			updates.append("role_id = ?")
			params.append(role_id)

		if phone is not None:
			updates.append("phone = ?")
			params.append(phone)

		if address is not None:
			updates.append("address = ?")
			params.append(address)

		if not updates:
			return True

		updates.append("updated_at = CURRENT_TIMESTAMP")
		params.append(employee_id)
		query = f"""
			UPDATE "Employee" SET {', '.join(updates)}
			WHERE id = ?
		"""

		conn.execute(query, params)
		conn.commit()
		return True

    except Exception as e:
			conn.rollback()
			raise

def delete_employee(conn, employee_id: int) -> bool:
	"""Elimina un empleado (eliminación física)"""
	try:
		employee = get_employee_by_id(conn, employee_id)
		if employee is None:
			return False

		conn.execute("""
			DELETE FROM "Employee" WHERE id = ?
		""", (employee_id,))
		conn.commit()
		return True

	except Exception as e:
		conn.rollback()
		raise


def desactivate_employee(conn, employee_id: int) -> bool:
    """Desactiva un empleado (eliminación lógica)"""
	try:
		employee = get_employee_by_id(conn, employee_id)
		if employee is None:
			return False

		conn.execute("""
			UPDATE "Employee" SET active = 0, updated_at = CURRENT_TIMESTAMP
			WHERE id = ?
		""", (employee_id,))
		conn.commit()
		logger.info(f"Empleado desactivado: {employee_id}")
		return True

	except Exception as e:
		conn.rollback()
		raise


def activate_employee(conn, employee_id: int) -> bool:
	"""Activa un empleado desactivado"""
	try:
		employee = get_employee_by_id(conn, employee_id)
		if employee is None:
			return False

		conn.execute("""
			UPDATE "Employee" SET active = 1, updated_at = CURRENT_TIMESTAMP
			WHERE id = ?
		""", (employee_id,))
		conn.commit()
    return True

	except Exception as e:
		conn.rollback()
    raise
