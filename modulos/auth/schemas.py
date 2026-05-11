from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# ==========================================
# REQUESTS (Lo que llega del cliente)
# ==========================================

class UserRegister(BaseModel):
	"""Datos para registrar un nuevo usuario"""
	email: EmailStr
	rut: Optional[str] = Field(default=None,
			min_length=7,
			max_length=12,
			description="RUT/Documento de identidad (ej: 12345678-K o 12345678K)"
	)
	password: str = Field(min_length=12, description="Mínimo 12 caracteres")
	full_name: str = Field(min_length=2)
	role_id: int = Field(default=1, description="1=barista, 0=admin")

class UserLogin(BaseModel):
	"""Credenciales para login"""
	email: EmailStr
	password: str

# ==========================================
# RESPONSES (Lo que retorna el servidor)
# ==========================================

class UserResponse(BaseModel):
	"""Usuario sin contraseña (para respuestas)"""
	id: int
	email: str
	full_name: str
	role_id: int
	active: bool
	rut: Optional[str] = None

	class Config:
		from_attributes = True

class TokenResponse(BaseModel):
	"""Respuesta con tokens"""
	access_token: str
	refresh_token: str
	token_type: str = "bearer"
	user: UserResponse

class TokenRefreshRequest(BaseModel):
	"""Request para refrescar token"""
	refresh_token: str


class UserUpdate(BaseModel):
	"""Datos para actualizar un usuario"""
	email: Optional[EmailStr] = None
	rut: Optional[str] = Field(
		min_length=7,
		max_length=12,
		description="RUT/Documento de identidad (ej: 12345678-K o 12345678K)"
	)
	full_name: Optional[str] = Field(
		None,
		min_length=2,
		max_length=100
	)
	role_id: Optional[int] = Field(
		None,
		description="0=admin, 1=barista"
	)

	class Config:
		json_schema_extra = {
			"example": {
				"rut": "12345678-K",
				"email": "new_email@cafe-pulento.com",
				"full_name": "León Leonino Leoncio",
				"role_id": 0
			}
		}


class UserStatusUpdate(BaseModel):
	"""Datos para cambiar el estado de un usuario"""
	active: bool = Field(description="True para activar, False para desactivar")

	class Config:
		json_schema_extra = {
			"example": {
				"active": False
			}
		}


class UserListResponse(BaseModel):
	"""Respuesta con lista de usuarios"""
	users: list[UserResponse]
	total: int

	class Config:
		json_schema_extra = {
			"example": {
				"users": [
					{
						"id": 1,
						"rut": "12345678-K",
						"email": "juan@cafe.com",
						"full_name": "Juan Pérez",
						"role_id": 1,
						"active": True
					}
				],
			"total": 1
			}
	}


class DeleteResponse(BaseModel):
	"""Respuesta de eliminación exitosa"""
	message: str
	user_id: int

	class Config:
		json_schema_extra = {
			"example": {
				"message": "Usuario eliminado exitosamente",
				"user_id": 1
			}
		}


class StatusUpdateResponse(BaseModel):
	"""Respuesta de cambio de estado"""
	message: str
	user_id: int
	active: bool

	class Config:
		json_schema_extra = {
			"example": {
				"message": "Estado del usuario actualizado",
				"user_id": 1,
				"active": False
			}
		}
