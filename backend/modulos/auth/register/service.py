#-------------------------------
# Modulos y librerías
#-------------------------------
from fastapi import HTTPException
from shared.database import get_connection
from shared.security.hash import hash_password
from shared.security.jwt_handler import create_access_token, create_refresh_token
from modulos.auth.schemas import UserRegister, TokenResponse, UserResponse
from modulos.auth.repository import (
  user_exists, user_rut_exists, create_user, get_user_by_id
  )

#----------------
# Manejo de errores
#----------------
import logging

logger = logging.getLogger(__name__)

#----------------
# SERVICE REGISTER
#----------------

def register_user(data: UserRegister):
  """
  Registra un nuevo usuario del sistema. Maneja toda la lógica de registros y validaciones.
	returns: TokenResponse con tokens y datos del usuario
  """
  conn = get_connection()

  try:
    # ========== INICIAR TRANSACCIÓN ==========
    conn.execute("BEGIN")
    logger.info(f"Iniciando registro para: {data.email}")

    # ========== VALIDACIONES ==========

    # Validar que el email no exista
    if user_exists(conn, data.email):
      logger.warning(f"Email duplicado: {data.email}")
      conn.rollback()
      raise HTTPException(
        status_code=400,
        detail="Email ya registrado"
      )

    # Validar RUT si se proporciona
    if data.rut and user_rut_exists(conn, data.rut):
      logger.warning(f"RUT duplicado: {data.rut}")
      conn.rollback()
      raise HTTPException(
        status_code=400,
        detail="RUT ya registrado"
      )

    # Validar role_id
    if data.role_id not in [0, 1, 2, 3, 4]:
      logger.warning(f"role_id inválido: {data.role_id}")
      conn.rollback()
      raise HTTPException(
        status_code=400,
        detail="role_id inválido"
      )

    # ========== PROCESAMIENTO ==========

    # Hashear contraseña
    hashed_password = hash_password(data.password)
    logger.debug(f"Contraseña hasheada para: {data.email}")

    # Crear usuario
    try:
      user_id = create_user(
        conn,
        email=data.email,
        hashed_password=hashed_password,
        full_name=data.full_name,
        role_id=data.role_id,
        rut=data.rut
      )
      logger.info(f"Usuario insertado: {data.email} (ID: {user_id})")
    except Exception as e:
      logger.error(f"Error al insertar usuario: {str(e)}")
      conn.rollback()
      raise HTTPException(
        status_code=500,
        detail="Error al crear usuario en BD"
      )

    # Obtener datos del usuario creado
    try:
      user = get_user_by_id(conn, user_id)
    except Exception as e:
      logger.error(f"Error al obtener usuario: {str(e)}")
      conn.rollback()
      raise HTTPException(
        status_code=500,
        detail="Error al recuperar datos del usuario"
      )

    if user is None:
      logger.error(f"Usuario creado pero no recuperable: {user_id}")
      conn.rollback()
      raise HTTPException(
        status_code=500,
        detail="Error al recuperar datos del usuario creado"
      )

    # Crear tokens
    try:
      access_token = create_access_token({
        "sub": str(user["id"]),
        "email": user["email"]
      })
      refresh_token = create_refresh_token({
        "sub": str(user["id"])
      })
      logger.debug(f"Tokens creados para usuario: {user_id}")
    except Exception as e:
      logger.error(f"Error al crear tokens: {str(e)}")
      conn.rollback()
      raise HTTPException(
        status_code=500,
        detail="Error al generar tokens"
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
    except Exception as e:
      logger.error(f"Error al construir respuesta: {str(e)}")
      logger.error(f"User dict keys: {user.keys() if user else 'None'}")
      conn.rollback()
      raise HTTPException(
        status_code=500,
        detail="Error al procesar datos del usuario"
      )

    # ========== COMMIT TRANSACCIÓN ==========
    conn.commit()
    logger.info(f"Registro exitoso: {user['email']} (ID: {user_id})")

    return TokenResponse(
      access_token=access_token,
      refresh_token=refresh_token,
      user=user_response
    )

  except HTTPException:
    raise

  except Exception as e:
    logger.error(f"Error inesperado en registro: {str(e)}", exc_info=True)
    try:
      conn.rollback()
      logger.info("Transacción revocada")
    except Exception as rollback_error:
      logger.error(f"Error al hacer rollback: {rollback_error}")

    raise HTTPException(
      status_code=500,
      detail="Error al registrar usuario"
    )

  finally:
    conn.close()

