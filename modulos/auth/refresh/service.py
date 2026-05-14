from fastapi import HTTPException
from shared.security.jwt_handler import verify_token, create_access_token
from shared.database import get_connection
from modulos.auth.schemas import TokenRefreshRequest, TokenResponse, UserResponse
from modulos.auth.repository import get_user_by_id

def refresh_access_token(data: TokenRefreshRequest):
	"""Genera un nuevo access token usando el refresh token"""

	# Verificar refresh token
	payload = verify_token(data.refresh_token)
	if payload is None:
		raise HTTPException(
			status_code=401,
			detail="Refresh token inválido o expirado."
		)

	user_id = int(payload.get("sub"))

	# Obtener usuario actual
	conn = get_connection()
	try:
		user = get_user_by_id(conn, user_id)
		# Chequea usuario primero
		if user is None or not user["active"]:
			raise HTTPException(
				status_code=401,
				detail="Usuario no válido"
			)
		# Crear nuevo access token
		access_token = create_access_token({"sub": str(user["id"]), "email": user["email"]})
		# Crea respuesta
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
			refresh_token=data.refresh_token,  # Reutilizar mismo refresh token
			user=user_response
		)
	finally:
			conn.close()
