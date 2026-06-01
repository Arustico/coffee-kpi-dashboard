from fastapi import HTTPException
from shared.database import get_connection

from modulos.auth.schemas import (
	EmployeeCreate, EmployeeUpdate, EmployeeResponse,
	EmployeeListResponse, DeleteResponse, StatusUpdateResponse)

from modulos.employees.repository import (
	employee_rut_exists, create_employee, get_employee_by_id,
	get_all_employees, get_active_employees, update_employee,
	delete_employee, desactivate_employee, activate_employee)


#------------------------------------------
# SERVICES EMPLOYEES
#------------------------------------------

#------------------------------------------
# CREA nuevo empleado
#------------------------------------------
def create_employee_service(data: EmployeeCreate, admin_user):
	"""Crea un nuevo empleado"""
	conn = get_connection()

	try:
		# Validar que el RUT no exista
		if employee_rut_exists(conn, data.rut):
			raise HTTPException(
				status_code=400,
				detail="RUT ya registrado"
			)

		# Crear empleado
		employee_id = create_employee(
			conn,
			full_name=data.full_name,
			rut=data.rut,
			role_id=data.role_id,
			user_id=data.user_id,
			phone=data.phone,
			address=data.address
		)

		# Obtener empleado creado
		employee = get_employee_by_id(conn, employee_id)
		return EmployeeResponse(
			id=employee["id"],
			full_name=employee["full_name"],
			rut=employee["rut"],
			role_id=employee["role_id"],
			user_id=employee["user_id"],
			active=bool(employee["active"]),
			phone=employee["phone"],
			address=employee["address"],
			hire_date=employee["hire_date"],
			created_at=employee["created_at"]
		)
	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail="Error al crear empleado"
		)
	finally:
		conn.close()

#------------------------------------------
# GET todos los empleados
#------------------------------------------
def get_all_employees_service():
	"""Obtiene lista de todos los empleados"""
	conn = get_connection()
	try:
		rows = get_all_employees(conn)
		employees = []
		for row in rows:
			employees.append(
				EmployeeResponse(
					id=row["id"],
					full_name=row["full_name"],
					rut=row["rut"],
					role_id=row["role_id"],
					user_id=row["user_id"],
					active=bool(row["active"]),
					phone=row["phone"],
					address=row["address"],
					hire_date=row["hire_date"],
					created_at=row["created_at"]
				)
			)

		return EmployeeListResponse(
			employees=employees,
			total=len(employees)
		)

	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail="Error al obtener empleados"
		)
	finally:
		conn.close()

#------------------------------------------
# GET empleados activos
#------------------------------------------
def get_active_employees_service():
	"""Obtiene lista de empleados activos"""
	conn = get_connection()

	try:
		rows = get_active_employees(conn)
		employees = [ EmployeeResponse(
			id=row["id"],
			full_name=row["full_name"],
			rut=row["rut"],
			role_id=row["role_id"],
			user_id=row["user_id"],
			active=bool(row["active"]),
			phone=row["phone"],
			address=row["address"],
			hire_date=row["hire_date"],
			created_at=row["created_at"]) for row in rows]

		return EmployeeListResponse(
			employees=employees,
			total=len(employees)
		)

	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail="Error al obtener empleados activos")
	finally:
		conn.close()

#------------------------------------------
# GET datos de un empleado
#------------------------------------------
def get_employee_service(employee_id: int):
	"""Obtiene datos de un empleado específico"""
	conn = get_connection()

	try:
		employee = get_employee_by_id(conn, employee_id)
		if employee is None:
			raise HTTPException(
				status_code=404,
				detail="Empleado no encontrado")

		response = EmployeeResponse(
			id=employee["id"],
			full_name=employee["full_name"],
			rut=employee["rut"],
			role_id=employee["role_id"],
			user_id=employee["user_id"],
			active=bool(employee["active"]),
			phone=employee["phone"],
			address=employee["address"],
			hire_date=employee["hire_date"],
			created_at=employee["created_at"])
		return response

	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail="Error al obtener empleado"
			)
	finally:
		conn.close()

#------------------------------------------
# UPDATE datos de empleado
#------------------------------------------
def update_employee_service(employee_id: int, data: EmployeeUpdate, admin_user):
	"""Actualiza datos de un empleado"""
	conn = get_connection()
	try:
	# Actualizar empleado
		success = update_employee(
			conn,
			employee_id,
			full_name=data.full_name,
			rut=data.rut,
			role_id=data.role_id,
			phone=data.phone,
			address=data.address
		)

		if not success:
			raise HTTPException(
				status_code=404,
				detail="Empleado no encontrado"
			)

	# Obtener empleado actualizado
		employee = get_employee_by_id(conn, employee_id)
		response = EmployeeResponse(
			id=employee["id"],
			full_name=employee["full_name"],
			rut=employee["rut"],
			role_id=employee["role_id"],
			user_id=employee["user_id"],
			active=bool(employee["active"]),
			phone=employee["phone"],
			address=employee["address"],
			hire_date=employee["hire_date"],
			created_at=employee["created_at"]
		)
		return response

	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail="Error al actualizar empleado"
		)
	finally:
		conn.close()

#------------------------------------------
# DEL empleado permanentemente
#------------------------------------------
def delete_employee_service(employee_id: int, admin_user):
	"""Elimina un empleado"""
	conn = get_connection()
	try:
		success = delete_employee(conn, employee_id)

		if not success:
			raise HTTPException(
				status_code=404,
				detail="Empleado no encontrado")

		return DeleteResponse(
			message="Empleado eliminado exitosamente",
			id=employee_id)

	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail="Error al eliminar empleado")

	finally:
		conn.close()

#------------------------------------------
# UPDATE estado de un empleado
#------------------------------------------
def update_employee_status_service(employee_id: int, active: bool, admin_user):
	"""Activa o desactiva un empleado"""
	conn = get_connection()

	try:
		if active:
			success = activate_employee(conn, employee_id)
		else:
			success = soft_delete_employee(conn, employee_id)

		if not success:
			raise HTTPException(
				status_code=404,
				detail="Empleado no encontrado")

		action = "activado" if active else "desactivado"
		return StatusUpdateResponse(
			message=f"Empleado {action} exitosamente",
			id=employee_id,
			active=active)

	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail="Error al cambiar estado del empleado")

	finally:
		conn.close()


