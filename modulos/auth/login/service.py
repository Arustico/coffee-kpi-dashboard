from fastapi import HTTPException
from shared.database import get_connection
from shared.security.hash import verify_password
from shared.security.jwt_handler import create_access_token, create_refresh_token
from modulos.auth.schemas import UserLogin, TokenResponse, UserResponse
from modulos.auth.repository import get_user_by_email, update_last_login

    )
#-----------------
# SERVICE LOGIN
#-----------------

def login_user(data: UserLogin):
	"""Autentica un usuario y retorna tokens"""
	conn = get_connection()

	try:
		# Buscar usuario por email
		user = get_user_by_email(conn, data.email)
		# Si user no existe
		if user is None:
			raise HTTPException(
					status_code=401,
					detail="Credenciales inválidas: Email incorrecto"
			)
		# Validar contraseña
		if not verify_password(data.password, user["hashed_password"]):
			raise HTTPException(
				status_code=401,
				detail="Credenciales inválidas: Contraseña incorrecta"
			)

		# Verificar que usuario está activo
		if not user["active"]:
			raise HTTPException(
				status_code=403,
				detail="Usuario inactivo"
			)

		# Actualizar último login
		update_last_login(conn, user["id"])

		# Crear tokens
		access_token = create_access_token({"sub": str(user["id"]), "email": user["email"]})
		refresh_token = create_refresh_token({"sub": str(user["id"])})

		# Construir respuesta
		user_response = UserResponse(
			id=user["id"],
			email=user["email"],
			full_name=user["full_name"],
			role_id=user["role_id"],
			active=bool(user["active"])
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
			detail=f"Error en autenticación"
		)
	finally:
		conn.close()


def update_last_login(conn, user_id: int):
	"""Actualiza el último login del usuario"""
	try:
		conn.execute("""
			UPDATE "User" SET updated_at = CURRENT_TIMESTAMP
			WHERE id = ?
		""", (user_id,))
		conn.commit()
	except Exception as e:
		raise
