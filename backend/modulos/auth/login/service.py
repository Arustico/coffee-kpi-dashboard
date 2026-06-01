from fastapi import HTTPException
from shared.database import get_connection
from shared.security.hash import verify_password
from shared.security.jwt_handler import create_access_token, create_refresh_token
from modulos.auth.schemas import UserLogin, TokenResponse, UserResponse
from modulos.auth.repository import get_user_by_email, update_user_last_login

#-------------------
# Manejo de errores
#-------------------
import logging
logger = logging.getLogger(__name__)

#-----------------
# SERVICE LOGIN
#-----------------

def login_user(data: UserLogin):
	"""Autentica un usuario y retorna tokens"""
	conn = get_connection()

	try: # Intento general
		conn.execute("BEGIN")
		# Buscar usuario por email
		try:
			user = get_user_by_email(conn, data.email)
		except Exception as e:
			logger.error(f"Error al buscar usuario: {str(e)}")
			conn.rollback()
			raise HTTPException(
					status_code=500,
					detail="Error al buscar usuario"
			)
		if user is None:
			logger.warning(f"Email no encontrado: {data.email}")
			conn.rollback()
			raise HTTPException(
				status_code=401,
				detail="Credenciales inválidas"
			)

		# Validación de contraseña
		try:
			password_valid = verify_password(data.password, user["hashed_password"])
		except Exception as e:
			logger.error(f"Error al verificar contraseña: {str(e)}")
			conn.rollback()
			raise HTTPException(
				status_code=500,
				detail="Error al verificar credenciales"
				)
		if not password_valid:
			logger.warning(f"Contraseña incorrecta: {data.email}")
			conn.rollback()
			raise HTTPException(
				status_code=401,
				detail="Credenciales inválidas")

		# Verificación que usuario está activo
		if not user["active"]:
			logger.warning(f"Usuario inactivo: {data.email}")
			conn.rollback()
			raise HTTPException(
				status_code=403,
				detail="Usuario inactivo")

		# Si todo sale bien, actualizamos el login
		# Actualizar último login
		try:
			update_user_last_login(conn, user["id"])
			logger.debug(f"Último login actualizado: {user['id']}")
		except Exception as e:
			logger.error(f"Error al actualizar último login: {str(e)}")
			logger.warning("Continuando a pesar de error no crítico")

		# Crear los tokens
		try:
			access_token = create_access_token({
				"sub": str(user["id"]),
				"email": user["email"]})
			refresh_token = create_refresh_token({
				"sub": str(user["id"])})
			# Información desorrallor
			logger.debug(f"Tokens creados para: {user['email']}")

		except Exception as e:
			logger.error(f"Error al crear tokens: {str(e)}")
			conn.rollback()
			raise HTTPException(
				status_code=500,
				detail="Error al generar tokens")
		# Si sale bien, se construye respuesta
		# Construir respuesta
		try:
			user_response = UserResponse(
				id=user["id"],
				email=user["email"],
				full_name=user["full_name"],
				rut=user["rut"],
				role_id=user["role_id"],
				active=bool(user["active"]),
				created_at=user["created_at"]
				)
		except Exception as e:
			logger.error(f"Error al construir respuesta: {str(e)}")
			conn.rollback()
			raise HTTPException(
				status_code=500,
				detail="Error al procesar datos del usuario")
		# Si no hay errores, enviamos commit
		conn.commit()
		logger.info(f"Login exitoso: {user['email']}")
		response = TokenResponse(
			access_token=access_token,
			refresh_token=refresh_token,
			user=user_response)
		return response
	# Excepciones generales
	except HTTPException:
		raise
	except Exception as e:
		logger.error(f"Error inesperado en login: {str(e)}", exc_info=True)
		try:
			conn.rollback()
			logger.info("Login revocado.")
		except Exception as rollback_error:
			logger.error(f"Error al hacer rollback: {rollback_error}")
			raise HTTPException(
				status_code=500,
				detail="Error en autenticación")
	# Finalmente general
	finally:
		conn.close()
