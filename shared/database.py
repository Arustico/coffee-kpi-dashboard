#============================
# Conecta a la base de datos, de no existir crea una
#============================
import os
import logging
from dotenv import load_dotenv
from pathlib import Path

import sqlite3

# ─────────────────────────────────────────────
# Configuración de entorno y logging
# ─────────────────────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# Variables de entorno
# ─────────────────────────────────────────────
load_dotenv()
BD_PATH = Path(os.getenv("BD_PATH"))
SCHEMA_PATH = Path(os.getenv("SCHEMA_PATH"))
VIEWS_PATH = Path(os.getenv("VIEWS_PATH"))

# ─────────────────────────────────────────────
# Funciones
# ─────────────────────────────────────────────
def init_db():
  """
  Inicia la base de datos y carga la lógica y el esquema.
  """
  conn = get_connection()
  logger.info("Cargando esquema y vistas de la base de datos...")

  with open(SCHEMA_PATH) as f:
    conn.executescript(f.read())

  with open(VIEWS_PATH) as f:
    conn.executescript(f.read())

  conn.close()
  print("BD creada + schema cargado")

def get_connection():
  logger.info("Conectandose a base de datos...")
  conn = sqlite3.connect(BD_PATH)
  conn.row_factory = sqlite3.Row
  conn.execute("PRAGMA foreign_keys = ON;")
  logger.info("Conexión OK")
  return conn

if __name__ == "__main__":
  init_db()
  get_connection()
