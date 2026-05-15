# Modulo para registrar un nuevo usuario

# Librerias
from fastapi import HTTPException
from shared.database import get_connection
from shared.security.hash import hash_password
from shared.security.jwt_handler import create_access_token, create_refresh_token
from modulos.auth.schemas import UserRegister, TokenResponse, UserResponse
from modulos.auth.repository import user_exists, create_user, create_user, get_user_by_id


#-----------------
# SERVICE REGISTER
#-----------------

def register_user(data: UserRegister):
	"""Registra un nuevo usuario. Return: TokenResponse con tokens y datos del usuario """
	conn = get_connection()
	try:
		# Validar que el email no exista
		if user_exists(conn, data.email):
			raise HTTPException(
				status_code=400,
				detail="Email ya registrado"
			)

		# Validar RUT si se proporciona
		if data.rut and user_rut_exists(conn, data.rut):
			logger.warning(f"Intento de registro con RUT duplicado: {data.rut}")
			raise HTTPException(
				status_code=400,
				detail="RUT ya registrado"
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
		# Obtener datos del usuario creado
		user = get_user_by_id(conn, user_id)

		# Crear tokens
		access_token = create_access_token({
			"sub": str(user["id"]),
			"email": user["email"]
		})
		refresh_token = create_refresh_token({
			"sub": str(user["id"])
		})

		# Construir respuesta
		user_response = UserResponse(
			id=user["id"],
			email=user["email"],
			full_name=user["full_name"],
			rut=user["rut"],
			role_id=user["role_id"],
			active=bool(user["active"]),
			created_at=user["created_at"]
		)

		return TokenResponse(
			access_token=access_token,
			refresh_token=refresh_token,
			user=user_response
		)

	except HTTPException:
		raise
	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail="Error al registrar usuario"
		)
	finally:
		conn.close()

