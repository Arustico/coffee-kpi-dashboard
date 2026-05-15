from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from shared.security.jwt_handler import verify_token
from shared.database import get_connection
from modulos.auth.repository import get_user_by_id

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
	"""
		Valida el token JWT y retorna el usuario actual
		Esta función actúa como GUARDIÁN: Se ejecuta ANTES de cualquier endpoint protegido.
	"""

	token = credentials.credentials
	payload = verify_token(token)
	# Si no existe el payload entonces error.
	if payload is None:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Token inválido o expirado",
			headers={"WWW-Authenticate": "Bearer"},
		)
	# sino, obtenemos identificacion del usuario
	user_id = int(payload.get("sub")) #"sub" -> "subject" (el sujeto == usuario del token)

	conn = get_connection()
	try:
		user = get_user_by_id(conn, user_id)
		# Chequea si usuario existe
		if user is None:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Usuario no encontrado"
			)
		# Todo ok, devuelve datos del usuario
		return user
	finally:
		conn.close()

# Misma función para administrador
async def get_current_admin(current_user = Depends(get_current_user)):
	"""Valida que el usuario sea admin"""
	if current_user["role_id"] != 0: # role_id: 0=admin, 1=barista
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Se requieren permisos de administrador"
		)
	return current_user
