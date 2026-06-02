"""
Script para crear el primer usuario admin
Ejecutar solo una vez al inicializar el proyecto
"""
from shared.database import get_connection
from shared.security.hash import hash_password
from modulos.auth.repository.user_repository import create_user, user_exists
from os import getenv

# VARIABLES DE ENTORNO
EMAIL_ADMIN = getenv("EMAIL_ADMIN_ZERO")
ADMIN_PASSWD  = getenv("SECRET_PASSWD")

# LOGS ERRORES
import logging
logger = logging.getLogger(__name__)


def create_admin():
  """Crea el primer usuario admin"""
  conn = get_connection()
  
  try:
    # Verificar si ya existe un admin
    admin_check = conn.execute(
      'SELECT id FROM "User" WHERE role_id = 0 LIMIT 1'
    ).fetchone()
    
    if admin_check:
      logger.info("Ya existe un usuario admin en la BD")
      return
    
    # Crear admin
    email = EMAIL_ADMIN
    password = ADMIN_PASSWD
    full_name = "Administrador"
    role_id = 0  # Admin
    
    # Verificar que el email no existe
    if user_exists(conn, email):
      logger.error(f"El email {email} ya existe")
      return
    
    # Hashear contraseña
    hashed_password = hash_password(password)
    
    # Crear usuario
    user_id = create_user(
      conn,
      email=email,
      hashed_password=hashed_password,
      full_name=full_name,
      role_id=role_id
    )
    
    conn.commit()
    
    print("\n" + "="*50)
    logger.info("USUARIO ADMIN CREADO EXITOSAMENTE")
    logger.info(f"Email: {email}")
    logger.info(f"Role: Admin (ID: {role_id})")    
    return user_id
  
  except Exception as e:
    logger.error(f"Error al crear admin: {str(e)}")
    conn.rollback()
    raise
  finally:
    conn.close()

if __name__ == "__main__":
  create_admin()