# ─────────────────────────────────────────────
"""
Simula datos de operaciones para poblar base de datos. Ayuda a probar si todo está correcto:
    1. probar schema -> ver si FK funciona
    2. probar dashboard -> tener ventas falsas
    3. probar KPIs -> generar desperdicio
    4. desarrollo -> no escribir datos manualmente

FLUJO DE POPULACIÓN:
        Role
        ↓
        Employee
        ↓
        Turno
        ↓
        IngredientUnit
        ↓
        Ingredient
        ↓
        Product
        ↓
        Receta (ProductIngredient)
        ↓
        Sale
        ↓
        SaleItem
"""

import os
import sys
from dotenv import load_dotenv
from pathlib import Path
# ─────────────────────────────────────────────
# Variables de entorno
# ─────────────────────────────────────────────
load_dotenv()
FOLDER_PRJCT = os.getenv("FOLDER_PRJCT")
# se agrega para poder carcar librería shared
sys.path.append(FOLDER_PRJCT)

from shared.database import get_connection

def seed():
    conn = get_connection()
    conn.execute("PRAGMA foreign_keys = ON;")

    # Roles
    conn.execute("INSERT INTO Role (id, name) VALUES (?, ?)", (0, "admin",))
    conn.execute("INSERT INTO Role (id, name) VALUES (?, ?)", (1, "barista",))

    # Empleado
    conn.execute("""
        INSERT INTO Employee (name, role_id)
        VALUES (?, ?)
    """, ("Juan", 1))

    # Turno
    conn.execute("""
        INSERT INTO Turn (label, start_time, end_time)
        VALUES (?, ?, ?)
    """, ("Mañana", "08:00", "14:00"))

    # Unidad Ingrediente
    conn.execute("""
        INSERT INTO IngredientUnit (unit)
        VALUES (?)
    """, ("ml",))

    # Ingrediente
    conn.execute("""
        INSERT INTO Ingredient (name, unit)
        VALUES (?, ?)
    """, ("Leche", "ml"))

    # Producto
    conn.execute("""
        INSERT INTO Product (name, category, base_price)
        VALUES (?, ?, ?)
    """, ("Latte", "café", 3000))

    # Receta (ProductIngredient)
    conn.execute("""
        INSERT INTO ProductIngredient (product_id, ingredient_id, quantity)
        VALUES (?, ?, ?)
    """, (1, 1, 200))

    # Compra
    conn.execute("""
        INSERT INTO IngredientPurchase (ingredient_id, quantity, unit_cost, purchased_at)
        VALUES (?, ?, ?, datetime('now'))
    """, (1, 1000, 1.2))

    # Venta
    conn.execute("""
        INSERT INTO Sale (employee_id, turn_id, sold_at, total_amount)
        VALUES (?, ?, datetime('now'), ?)
    """, (1, 1, 3000))

    # Item
    conn.execute("""
        INSERT INTO SaleItem (sale_id, product_id, quantity, unit_price)
        VALUES (?, ?, ?, ?)
    """, (1, 1, 1, 3000))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed()
