"""
Seed script — Genera datos realistas de operación de cafetería.

Puebla la base de datos con ~30 días de operación simulada:
  - Roles, usuarios, empleados, turnos
  - Productos, ingredientes, unidades, recetas
  - Proveedores, compras de insumos
  - Ventas diarias con múltiples items
  - Registros de merma/desperdicio

Ejecutar después de haber creado la BD con:
  python shared/database.py

Uso:
  python scripts/seed_data.py
"""

import os
import sys
import random
import logging
from datetime import datetime, timedelta, date, time
from pathlib import Path


# Determinar raíz del backend (independiente de .env)
BACKEND_DIR = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, BACKEND_DIR)
os.environ.setdefault("FOLDER_PRJCT", BACKEND_DIR)

from shared.database import get_connection, init_db
from shared.security.hash import hash_password

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

DIAS_OPERACION = 30
FECHA_INICIO = date(2026, 5, 1)

EMAIL_ADMIN = os.getenv("EMAIL_ADMIN_ZERO")
ADMIN_PASSWD  = os.getenv("SECRET_PASSWD")


# Semilla para reproducibilidad
random.seed(42)

# =============================================================================
# DATOS MAESTROS
# =============================================================================

ROLES = [
    (0, "admin"),
    (1, "barista"),
    (2, "contador")
]

TURNOS = [
    (1, "Mañana",  "08:00", "14:00"),
    (2, "Tarde",   "14:00", "20:00"),
    (3, "Noche",   "20:00", "02:00"),
]

UNIDADES = ["ml", "g", "u"]

USUARIOS = [
    (EMAIL_ADMIN,    ADMIN_PASSWD,     "Administrador",   0),
    ("juan@coffee.com",     "barista123",   "Juan Pérez",      1),
    ("maria@coffee.com",    "barista123",   "María García",    1),
    ("carlos@coffee.com",   "barista123",   "Carlos López",    1),
    ("ismael@externo.com",  "contador123",   "Ismael Lira",    2),
]

EMPLEADOS = [
    ("admin@coffee.com",  "Admin",        "1.111.111-1", 0),
    ("juan@coffee.com",   "Juan Pérez",   "2.222.222-2", 1),
    ("maria@coffee.com",  "María García", "3.333.333-3", 1),
    ("carlos@coffee.com", "Carlos López", "4.444.444-4", 1),
]

PRODUCTOS = [
    ("Espresso",    "café",    1800),
    ("Americano",   "café",    2200),
    ("Latte",       "café",    3200),
    ("Cappuccino",  "café",    3000),
    ("Mocha",       "café",    3500),
    ("Flat White",  "café",    3400),
    ("Cortado",     "café",    2500),
    ("Té",          "bebestible", 2000),
    ("Chai Latte",  "bebestible", 3500),
    ("Tostado",     "comida",  2500),
]

INGREDIENTES = [
    ("Café espresso",   "ml"),
    ("Leche entera",    "ml"),
    ("Agua mineral",    "ml"),
    ("Cacao en polvo",  "g"),
    ("Chocolate",       "g"),
    ("Miel",            "g"),
    ("Bolsa de té",     "u"),
    ("Bolsa de chai",   "u"),
    ("Pan",             "u"),
    ("Palta",           "g"),
    ("Tomate",          "g"),
]

RECETAS = [
    (1, 1, 20),    # Espresso: 20ml café
    (2, 1, 20),    # Americano: 20ml café
    (2, 3, 150),   # Americano: 150ml agua
    (3, 1, 20),    # Latte: 20ml café
    (3, 2, 200),   # Latte: 200ml leche
    (4, 1, 20),    # Cappuccino: 20ml café
    (4, 2, 150),   # Cappuccino: 150ml leche
    (4, 4, 10),    # Cappuccino: 10g cacao
    (5, 1, 20),    # Mocha: 20ml café
    (5, 2, 150),   # Mocha: 150ml leche
    (5, 5, 30),    # Mocha: 30g chocolate
    (6, 1, 40),    # Flat White: 40ml café
    (6, 2, 150),   # Flat White: 150ml leche
    (7, 1, 20),    # Cortado: 20ml café
    (7, 2, 60),    # Cortado: 60ml leche
    (8, 3, 200),   # Té: 200ml agua
    (8, 7, 1),     # Té: 1 bolsa
    (9, 2, 200),   # Chai latte: 200ml leche
    (9, 8, 1),     # Chai latte: 1 bolsa chai
    (9, 6, 20),    # Chai latte: 20g miel
    (10, 9, 1),    # Tostado: 1 pan
    (10, 10, 30),  # Tostado: 30g palta
    (10, 11, 50),  # Tostado: 50g tomate
]

PROVEEDORES = [
    "Café del Sur Ltda.",
    "Lácteos Premium SPA",
    "Distribuidora de Bebidas",
    "Panadería El Trigal",
    "Cacao y Especias Chile",
]

# Costos unitarios por ingrediente en cada compra (se varía para simular)
# (ingredient_id, proveedor_id, cantidad, costo_unitario)
COMPRAS_BASE = [
    (1, 1, 5000,  0.70),   # Café
    (2, 2, 20000, 0.12),   # Leche
    (3, 3, 50000, 0.01),   # Agua
    (4, 5, 2000,  2.50),   # Cacao
    (5, 5, 3000,  2.00),   # Chocolate
    (6, 5, 2000,  3.50),   # Miel
    (7, 3, 500,   120),    # Bolsa té
    (8, 3, 400,   180),    # Bolsa chai
    (9, 4, 600,   350),    # Pan
    (10, 4, 10000, 0.50),  # Palta
    (11, 4, 15000, 0.30),  # Tomate
]

# Probabilidades de productos por turno (suma ≤ 1.0 por turno)
# (producto_id, prob_mañana, prob_tarde, prob_noche)
PROB_PRODUCTOS = [
    (1,  0.08, 0.06, 0.12),   # Espresso
    (2,  0.10, 0.08, 0.10),   # Americano
    (3,  0.25, 0.22, 0.15),   # Latte
    (4,  0.15, 0.12, 0.08),   # Cappuccino
    (5,  0.10, 0.12, 0.08),   # Mocha
    (6,  0.05, 0.06, 0.04),   # Flat White
    (7,  0.05, 0.04, 0.06),   # Cortado
    (8,  0.05, 0.07, 0.05),   # Té
    (9,  0.07, 0.08, 0.06),   # Chai latte
    (10, 0.10, 0.15, 0.26),   # Tostado
]

VENTAS_POR_TURNO = {
    # (turno, dia_semana): (min_ventas, max_ventas, items_por_venta)
    # dia_semana: 0=lunes ... 6=domingo
    (1, 0): (15, 25),   # Mañana lunes
    (1, 1): (18, 28),
    (1, 2): (18, 28),
    (1, 3): (20, 30),
    (1, 4): (22, 32),
    (1, 5): (18, 28),
    (1, 6): (10, 18),
    (2, 0): (12, 20),
    (2, 1): (14, 22),
    (2, 2): (14, 22),
    (2, 3): (15, 24),
    (2, 4): (18, 26),
    (2, 5): (20, 30),
    (2, 6): (12, 20),
    (3, 0): (4, 10),
    (3, 1): (4, 10),
    (3, 2): (4, 10),
    (3, 3): (5, 12),
    (3, 4): (8, 15),
    (3, 5): (12, 22),
    (3, 6): (8, 14),
}

WASTE_REASONS = [
    "Leche vencida",
    "Café quemado",
    "Preparación incorrecta",
    "Derrame accidental",
    "Sobrante del día",
    "Producto en mal estado",
    "Error de receta",
]

# Probabilidad de registrar desperdicio por turno activo
WASTE_PROB = {
    1: 0.4,   # Mañana: 40%
    2: 0.5,   # Tarde: 50%
    3: 0.3,   # Noche: 30%
}


# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def random_time(turno_id, dia):
    """Genera un timestamp aleatorio dentro del horario del turno."""
    if turno_id == 1:
        h = random.randint(8, 13)
        m = random.randint(0, 59)
    elif turno_id == 2:
        h = random.randint(14, 19)
        m = random.randint(0, 59)
    else:
        h = random.randint(20, 23)
        m = random.randint(0, 59)
    dt = datetime.combine(dia, time(h, m, random.randint(0, 59)))
    if turno_id == 3 and h <= 2:
        dt += timedelta(days=1)
    return dt.isoformat()


def weighted_choice(turno_id):
    """Elige un producto según probabilidades del turno."""
    items = [(p[0], p[turno_id]) for p in PROB_PRODUCTOS]
    productos, pesos = zip(*items)
    return random.choices(productos, weights=pesos, k=1)[0]


def cantidad_por_producto(producto_id):
    """Simula la cantidad típica: 1 para bebidas, a veces 2 para comida."""
    if producto_id == 10:
        return random.choices([1, 2, 3], weights=[60, 30, 10])[0]
    return random.choices([1, 2, 3], weights=[75, 20, 5])[0]


# =============================================================================
# SEED PRINCIPAL
# =============================================================================

def seed():
    conn = get_connection()
    cur = conn.cursor()

    logger.info("🗑️  Limpiando datos existentes...")
    tablas = [
        "WasteLog", "SaleItem", "Sale",
        "IngredientPurchase", "Supplier",
        "ProductIngredient", "Ingredient", "IngredientUnit",
        "Product", "Turn", "Employee", '"User"', "Role",
    ]
    for t in tablas:
        cur.execute(f"DELETE FROM {t}")

    # ============================
    # 1. DIMENSIONALES
    # ============================
    logger.info("📦 Insertando roles...")
    for r_id, name in ROLES:
        cur.execute("INSERT INTO Role (id, name) VALUES (?, ?)", (r_id, name))

    logger.info("👤 Insertando usuarios...")
    for email, pw, nombre, role_id in USUARIOS:
        hashed = hash_password(pw)
        cur.execute(
            'INSERT INTO "User" (email, hashed_password, full_name, role_id) VALUES (?, ?, ?, ?)',
            (email, hashed, nombre, role_id),
        )

    logger.info("🧑‍🍳 Insertando empleados...")
    for email, nombre, rut, role_id in EMPLEADOS:
        user_row = cur.execute(
            'SELECT id FROM "User" WHERE email = ?', (email,)
        ).fetchone()
        cur.execute(
            """INSERT INTO Employee (full_name, rut, role_id, user_id, hire_date)
               VALUES (?, ?, ?, ?, ?)""",
            (nombre, rut, role_id, user_row["id"], FECHA_INICIO.isoformat()),
        )

    logger.info("🕐 Insertando turnos...")
    for t_id, label, start, end in TURNOS:
        cur.execute(
            "INSERT INTO Turn (id, label, start_time, end_time) VALUES (?, ?, ?, ?)",
            (t_id, label, start, end),
        )

    logger.info("📐 Insertando unidades de medida...")
    for unit in UNIDADES:
        cur.execute("INSERT INTO IngredientUnit (unit) VALUES (?)", (unit,))

    logger.info("🥛 Insertando ingredientes...")
    for name, unit in INGREDIENTES:
        cur.execute(
            "INSERT INTO Ingredient (name, unit) VALUES (?, ?)", (name, unit)
        )

    logger.info("☕ Insertando productos...")
    for name, cat, price in PRODUCTOS:
        cur.execute(
            "INSERT INTO Product (name, category, base_price) VALUES (?, ?, ?)",
            (name, cat, price),
        )

    logger.info("📝 Insertando recetas...")
    for prod_id, ing_id, qty in RECETAS:
        cur.execute(
            "INSERT INTO ProductIngredient (product_id, ingredient_id, quantity) VALUES (?, ?, ?)",
            (prod_id, ing_id, qty),
        )

    # ============================
    # 2. PROVEEDORES
    # ============================
    logger.info("🏢 Insertando proveedores...")
    for prov in PROVEEDORES:
        cur.execute("INSERT INTO Supplier (name) VALUES (?)", (prov,))

    # ============================
    # 3. COMPRAS DE INSUMOS (cada ~7 días)
    # ============================
    logger.info("📦 Insertando compras de insumos...")
    for ing_id, prov_id, qty_base, costo_base in COMPRAS_BASE:
        for semana in range(4):
            dia_compra = FECHA_INICIO + timedelta(days=semana * 7 + 1)
            variacion = random.uniform(-0.10, 0.12)
            costo = round(costo_base * (1 + variacion), 2)
            qty = qty_base * random.uniform(0.8, 1.2)
            cur.execute(
                """INSERT INTO IngredientPurchase
                       (ingredient_id, supplier_id, quantity, unit_cost, purchased_at)
                   VALUES (?, ?, ?, ?, ?)""",
                (ing_id, prov_id, round(qty, 2), costo, dia_compra.isoformat()),
            )

    # ============================
    # 4. VENTAS (simulación día a día)
    # ============================
    logger.info("💵 Insertando ventas...")
    total_ventas = 0
    for d in range(DIAS_OPERACION):
        dia = FECHA_INICIO + timedelta(days=d)
        dow = dia.weekday()

        for turno_id in (1, 2, 3):
            key = (turno_id, dow)
            rango = VENTAS_POR_TURNO.get(key)
            if not rango:
                continue
            min_v, max_v = rango
            num_ventas = random.randint(min_v, max_v)

            for _ in range(num_ventas):
                num_items = random.choices([1, 2, 3], weights=[55, 35, 10])[0]
                items = [weighted_choice(turno_id) for _ in range(num_items)]

                total = 0
                for prod_id in items:
                    precio_row = cur.execute(
                        "SELECT base_price FROM Product WHERE id = ?", (prod_id,)
                    ).fetchone()
                    precio = precio_row["base_price"]
                    qty_item = cantidad_por_producto(prod_id)
                    total += precio * qty_item

                empleado_id = random.choice([2, 3, 4])
                sold_at = random_time(turno_id, dia)

                cur.execute(
                    """INSERT INTO Sale (employee_id, turn_id, sold_at, total_amount)
                       VALUES (?, ?, ?, ?)""",
                    (empleado_id, turno_id, sold_at, total),
                )
                sale_id = cur.lastrowid

                for prod_id in items:
                    precio_row = cur.execute(
                        "SELECT base_price FROM Product WHERE id = ?", (prod_id,)
                    ).fetchone()
                    precio = precio_row["base_price"]
                    qty_item = cantidad_por_producto(prod_id)
                    cur.execute(
                        """INSERT INTO SaleItem (sale_id, product_id, quantity, unit_price)
                           VALUES (?, ?, ?, ?)""",
                        (sale_id, prod_id, qty_item, precio),
                    )

                total_ventas += 1

    # ============================
    # 5. MERMA / DESPERDICIO
    # ============================
    logger.info("🗑️  Insertando registros de merma...")
    total_mermas = 0
    for d in range(DIAS_OPERACION):
        dia = FECHA_INICIO + timedelta(days=d)
        dow = dia.weekday()

        for turno_id in (1, 2, 3):
            if random.random() > WASTE_PROB[turno_id]:
                continue

            num_mermas = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
            for _ in range(num_mermas):
                ing_id = random.choice([1, 2, 4, 5, 6, 9, 10, 11])

                if ing_id in (1, 2, 3):
                    qty = random.randint(50, 500)
                elif ing_id in (4, 5, 6):
                    qty = random.randint(10, 100)
                elif ing_id in (9,):
                    qty = random.randint(1, 5)
                else:
                    qty = random.randint(50, 500)

                empleado_id = random.choice([2, 3, 4])
                logged_at = random_time(turno_id, dia)
                razon = random.choice(WASTE_REASONS)

                cur.execute(
                    """INSERT INTO WasteLog
                           (ingredient_id, employee_id, turn_id, logged_at, quantity, reason)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (ing_id, empleado_id, turno_id, logged_at, qty, razon),
                )
                total_mermas += 1

    conn.commit()
    conn.close()

    logger.info("=" * 55)
    logger.info("✅ SEED COMPLETADO EXITOSAMENTE")
    logger.info(f"   📅 Días simulados:     {DIAS_OPERACION}")
    logger.info(f"   💵 Ventas creadas:     {total_ventas}")
    logger.info(f"   🗑️  Registros merma:   {total_mermas}")
    logger.info(f"   🏢 Proveedores:        {len(PROVEEDORES)}")
    logger.info(f"   ☕ Productos:           {len(PRODUCTOS)}")
    logger.info(f"   🥛 Ingredientes:       {len(INGREDIENTES)}")
    logger.info("=" * 55)


if __name__ == "__main__":
    seed()
