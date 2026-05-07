# Modulo para registrar un nuevo usuario

# Librerias
from fastapi import HTTPException
from shared.database import get_connection
from shared.security.hash import hash_password
from modulos.auth.schemas import UserRegister
from modulos.auth.repository import user_exists, create_user

def register_user(data: UserRegister):
	"""Registra un nuevo usuario"""
	conn = get_connection()
	try:
		# Validar que el email no exista
		if user_exists(conn, data.email):
			raise HTTPException(
				status_code=400,
				detail="Email ya registrado"
			)

		# Validar role_id válido
		if data.role_id not in [0, 1]:
			raise HTTPException(
				status_code=400,
				detail="role_id inválido (0=admin, 1=barista)"
		)

		# Hashear contraseña
		hashed_password = hash_password(data.password)

		# Crear usuario
		user_id = create_user(
			conn,
			email=data.email,
			hashed_password=hashed_password,
			full_name=data.full_name,
			role_id=data.role_id
		)

		return {
			"message": "Usuario registrado exitosamente",
			"user_id": user_id
		}

	except HTTPException:
		raise
	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail="Error al registrar usuario"
		)
	finally:
		conn.close()
