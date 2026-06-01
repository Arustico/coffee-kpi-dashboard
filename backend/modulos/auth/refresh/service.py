#-------------------------------
# Modulos y librerías
#-------------------------------
from fastapi import HTTPException
from shared.security.jwt_handler import verify_token, create_access_token
from shared.database import get_connection
from modulos.auth.schemas import TokenRefreshRequest, TokenResponse, UserResponse
from modulos.auth.repository import get_user_by_id

#-------------------------------
# Manejo de errores
#-------------------------------
import logging
logger = logging.getLogger(__name__)

#-------------------------------
# SERVICE REFRESH tokens
#-------------------------------
def refresh_access_token(data: TokenRefreshRequest):
	"""
	Genera un nuevo access token usando el refresh token. Maneja el refresh de tokens y validaciones
	"""
	conn = get_connection()

	try:
		# ========== INICIAR TRANSACCIÓN ==========
		conn.execute("BEGIN")
		logger.info("Iniciando refresh de token")

		# ========== VALIDACIONES ==========
		# Verificar refresh token
		try:
			payload = verify_token(data.refresh_token)
		except Exception as e:
			logger.error(f"Error al verificar token: {str(e)}")
			conn.rollback()
			raise HTTPException(
				status_code=500,
				detail="Error al verificar token"
				)

		if payload is None:
			logger.warning("Refresh token inválido o expirado")
			conn.rollback()
			raise HTTPException(
				status_code=401,
				detail="Refresh token inválido o expirado"
				)
		# Si todo ok entonces obtenemos usuario
		user_id = int(payload.get("sub"))
		logger.debug(f"Token válido para usuario: {user_id}")
		# ========== PROCESAMIENTO ==========
		# Obtener usuario actual
		try:
			user = get_user_by_id(conn, user_id)
		except Exception as e:
			logger.error(f"Error al obtener usuario: {str(e)}")
			conn.rollback()
			raise HTTPException(
					status_code=500,
					detail="Error al obtener usuario"
					)
		# Error si usuario no existe
		if user is None or not user["active"]:
			logger.warning(f"Usuario no válido: {user_id}")
			conn.rollback()
			raise HTTPException(
				status_code=401,
				detail="Usuario no válido"
				)

		# Crear nuevo access token
		try:
			access_token = create_access_token({
			"sub": str(user["id"]),
			"email": user["email"]
			})
			logger.debug(f"Access token creado para: {user['email']}")
		except Exception as e:
			logger.error(f"Error al crear access token: {str(e)}")
			conn.rollback()
			raise HTTPException(
				status_code=500,
				detail="Error al generar token"
				)

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
			logger.debug("Respuesta Refresh Token creada")
		except Exception as e:
			logger.error(f"Error al construir respuesta: {str(e)}")
			conn.rollback()
			raise HTTPException(
				status_code=500,
				detail="Error al procesar datos"
				)
		# ========== COMMIT TRANSACCIÓN ==========
		conn.commit()
		logger.info(f"Token refrescado exitosamente: {user['email']}")
		return TokenResponse(
			access_token=access_token,
			refresh_token=data.refresh_token,
			user=user_response
			)

	except HTTPException:
		raise
	except Exception as e:
		logger.error(f"Error inesperado en refresh: {str(e)}", exc_info=True)
		try:
			conn.rollback()
			logger.info("Refresh de tokens revocado")
		except Exception as rollback_error:
			logger.error(f"Error al hacer rollback: {rollback_error}")
			raise HTTPException(
				status_code=500,
				detail="Error al refrescar token"
				)
	finally:
		conn.close()
