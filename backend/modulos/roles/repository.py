"""
REPOSITORY LAYER - Roles & Permissions
Solo acceso a datos SQL
"""

# ==========================================
# PERMISSION REPOSITORY
# ==========================================

def create_permission(conn, role_id: int, module: str, action: str) -> int:
  """Inserta un nuevo permiso"""
  cursor = conn.execute("""
    INSERT INTO RolePermission (role_id, module, action)
    VALUES (?, ?, ?)
  """, (role_id, module, action))

  return cursor.lastrowid


def get_permission_by_id(conn, permission_id: int):
  """Obtiene un permiso por ID"""
  row = conn.execute("""
    SELECT id, role_id, module, action
    FROM RolePermission
    WHERE id = ?
  """, (permission_id,)).fetchone()

  return row


def get_permissions_by_role(conn, role_id: int):
  """Obtiene permisos de un rol"""
  rows = conn.execute("""
    SELECT id, role_id, module, action
    FROM RolePermission
    WHERE role_id = ?
    ORDER BY module, action
  """, (role_id,)).fetchall()

  return rows


def get_all_permissions(conn):
  """Obtiene todos los permisos"""
  rows = conn.execute("""
    SELECT id, role_id, module, action
    FROM RolePermission
    ORDER BY role_id, module, action
  """).fetchall()

  return rows


def permission_exists(conn, role_id: int, module: str, action: str) -> bool:
  """Verifica si un permiso existe"""
  row = conn.execute("""
    SELECT id FROM RolePermission
    WHERE role_id = ? AND module = ? AND action = ?
  """, (role_id, module, action)).fetchone()

  return row is not None


def delete_permission(conn, permission_id: int):
  """Elimina un permiso"""
  conn.execute("""
    DELETE FROM RolePermission WHERE id = ?
  """, (permission_id,))


def delete_permissions_by_role(conn, role_id: int):
  """Elimina todos los permisos de un rol"""
  conn.execute("""
    DELETE FROM RolePermission WHERE role_id = ?
  """, (role_id,))


def get_user_permissions(conn, user_id: int):
  """Obtiene permisos del usuario basado en su rol"""
  rows = conn.execute("""
    SELECT DISTINCT rp.module, rp.action
    FROM "User" u
    JOIN RolePermission rp ON u.role_id = rp.role_id
    WHERE u.id = ?
    ORDER BY rp.module, rp.action
  """, (user_id,)).fetchall()

  return rows


def user_has_permission(conn, user_id: int, module: str, action: str) -> bool:
  """Verifica si un usuario tiene permiso específico"""
  row = conn.execute("""
    SELECT 1
    FROM "User" u
    JOIN RolePermission rp ON u.role_id = rp.role_id
    WHERE u.id = ? AND rp.module = ? AND rp.action = ?
    LIMIT 1
  """, (user_id, module, action)).fetchone()

  return row is not None


def get_role_by_id(conn, role_id: int):
  """Obtiene un rol por ID"""
  row = conn.execute("""
    SELECT id, name
    FROM Role
    WHERE id = ?
  """, (role_id,)).fetchone()

  return row


def get_all_roles(conn):
  """Obtiene todos los roles"""
  rows = conn.execute("""
    SELECT id, name
    FROM Role
    ORDER BY name
  """).fetchall()

  return rows


def role_exists(conn, role_id: int) -> bool:
  """Verifica si un rol existe"""
  row = conn.execute("""
    SELECT id FROM Role WHERE id = ?
  """, (role_id,)).fetchone()

  return row is not None
