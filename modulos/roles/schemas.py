from pydantic import BaseModel, Field
from typing import List, Optional

# ==========================================
# ROLES SCHEMAS
# ==========================================

# ==========================================
# REQUESTS
# ==========================================

class RolePermissionCreate(BaseModel):
  """Crear permiso para un rol"""
  role_id: int = Field(gt=0, description="ID del rol")
  module: str = Field(min_length=1, max_length=50, description="Módulo (auth, sales, etc)")
  action: str = Field(min_length=1, max_length=50, description="Acción (create, read, update, delete)")

  class Config:
    json_schema_extra = {
      "example": {
        "role_id": 1,
        "module": "sales",
        "action": "create"
      }
    }


# ==========================================
# RESPONSES
# ==========================================

class PermissionResponse(BaseModel):
  """Respuesta de permiso"""
  id: int
  role_id: int
  module: str
  action: str

  class Config:
    from_attributes = True


class RoleWithPermissionsResponse(BaseModel):
  """Rol con sus permisos"""
  id: int
  name: str
  permissions: List[PermissionResponse] = []

  class Config:
    json_schema_extra = {
      "example": {
        "id": 0,
        "name": "Admin",
        "permissions": [
          {"id": 1, "role_id": 0, "module": "sales", "action": "create"},
          {"id": 2, "role_id": 0, "module": "sales", "action": "read"}
        ]
      }
    }


class UserPermissionsResponse(BaseModel):
  """Permisos del usuario actual"""
  user_id: int
  email: str
  role: str
  permissions: List[str] = Field(description="Lista de permisos en formato 'module:action'")

  class Config:
    json_schema_extra = {
      "example": {
        "user_id": 1,
        "email": "admin@cafe.com",
        "role": "Admin",
        "permissions": [
          "sales:create",
          "sales:read",
          "ingredients:create"
        ]
      }
    }


class PermissionCheckResponse(BaseModel):
  """Respuesta de verificación de permiso"""
  has_permission: bool
  message: str

  class Config:
    json_schema_extra = {
      "example": {
        "has_permission": True,
        "message": "Usuario tiene permiso para esta acción"
      }
    }
