from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# ==========================================
# REQUESTS - USER (Usuario del Sistema)
# ==========================================

class UserRegister(BaseModel):
	"""Datos para registrar un nuevo usuario del sistema"""
	email: EmailStr
	password: str = Field(
		min_length=8,
		max_length=128,
		description="Mínimo 8 caracteres"
	)
	full_name: str = Field(
		min_length=2,
		max_length=100,
		description="Nombre completo del usuario"
	)
	rut: Optional[str] = Field(
		None,
		min_length=7,
		max_length=12,
		description="RUT/Documento de identidad (opcional)"
	)
	role_id: int = Field(
		default=1,
		description="0=admin, 1=barista, 2=contador, 3=analista, etc."
	)

	class Config:
		json_schema_extra = {
			"example": {
				"email": "contador@cafe.com",
				"password": "MiPassword123!",
				"full_name": "León Leonidas",
				"rut": "12345678-K",  # Opcional
				"role_id": 2  # Contador
			}
		}


class UserLogin(BaseModel):
	"""Credenciales para login"""
	email: EmailStr
	password: str = Field(min_length=8)

	class Config:
		json_schema_extra = {
			"example": {
				"email": "contador@cafe.com",
				"password": "MiPassword123!"
			}
		}


class TokenRefreshRequest(BaseModel):
	"""Request para refrescar token"""
	refresh_token: str

	class Config:
		json_schema_extra = {
			"example": {
					"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
			}
		}


# ==========================================
# RESPONSES - USER
# ==========================================

class UserResponse(BaseModel):
	"""Usuario sin contraseña (para respuestas)"""
	id: int
	email: str
	full_name: str
	rut: Optional[str] = None
	role_id: int
	active: bool
	created_at: Optional[datetime] = None

	class Config:
		from_attributes = True


class TokenResponse(BaseModel):
	"""Respuesta con tokens después de login/register"""
	access_token: str
	refresh_token: str
	token_type: str = "bearer"
	user: UserResponse

	class Config:
		json_schema_extra = {
			"example": {
				"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
				"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
				"token_type": "bearer",
				"user": {
					"id": 1,
					"email": "contador@cafe.com",
					"full_name": "Carlos Gómez",
					"rut": "12345678-K",
					"role_id": 2,
					"active": True
					}
				}
		}


class RegisterResponse(BaseModel):
	"""Respuesta de registro exitoso"""
	message: str
	user_id: int

	class Config:
		json_schema_extra = {
			"example": {
				"message": "Usuario registrado exitosamente",
				"user_id": 1
			}
		}


class UserUpdate(BaseModel):
	"""Datos para actualizar un usuario"""
	email: Optional[EmailStr] = None
	rut: Optional[str] = Field(
		None,
		min_length=7,
		max_length=12,
		description="RUT/Documento de identidad (opcional)"
	)
	full_name: Optional[str] = Field(
		None,
		min_length=2,
		max_length=100
	)
	role_id: Optional[int] = Field(
		None,
		description="0=admin, 1=barista, 2=contador, 3=analista, etc."
	)

	class Config:
		json_schema_extra = {
			"example": {
				"email": "newemail@cafe.com",
				"rut": "87654321-A",
				"full_name": "Carlos Gómez Updated",
				"role_id": 2
				}
			}


class UserStatusUpdate(BaseModel):
	"""Datos para cambiar el estado de un usuario"""
	active: bool = Field(description="True para activar, False para desactivar")
	class Config:
		json_schema_extra = {
			"example": {"active": False}
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
						"email": "contador@cafe.com",
						"full_name": "Carlos Gómez",
						"rut": "12345678-K",
						"role_id": 2,
						"active": True
					}
				],
				"total": 1
			}
		}


# ==========================================
# REQUESTS - EMPLOYEE (Empleado/Trabajador)
# ==========================================

class EmployeeCreate(BaseModel):
	"""Datos para crear un nuevo empleado"""
	full_name: str = Field(
		min_length=2,
		max_length=100,
		description="Nombre completo del empleado"
	)
	rut: str = Field(
		min_length=7,
		max_length=12,
		description="RUT/Documento de identidad (obligatorio)"
	)
	role_id: int = Field(
		default=1,
		description="1=barista, 2=jefe turno, etc."
	)
	user_id: Optional[int] = Field(
		None,
		description="ID del usuario del sistema (opcional)"
	)
	phone: Optional[str] = Field(
		None,
		max_length=20,
		description="Teléfono de contacto"
	)
	address: Optional[str] = Field(
		None,
		max_length=255,
		description="Dirección"
	)

	class Config:
		json_schema_extra = {
			"example": {
				"full_name": "Juan Pérez",
				"rut": "12345678-K",
				"role_id": 1,
				"user_id": 1,  # Opcional
				"phone": "+56912345678",
				"address": "Calle Principal 123"
			}
		}


class EmployeeUpdate(BaseModel):
	"""Datos para actualizar un empleado"""
	full_name: Optional[str] = Field(
		None,
		min_length=2,
		max_length=100
	)
	rut: Optional[str] = Field(
		None,
		min_length=7,
		max_length=12,
		description="RUT (obligatorio si se crea empleado)"
	)
	role_id: Optional[int] = None
	phone: Optional[str] = Field(
		None,
		max_length=20
	)
	address: Optional[str] = Field(
		None,
		max_length=255
	)

	class Config:
		json_schema_extra = {
			"example": {
				"full_name": "Juan Pérez Actualizado",
				"rut": "87654321-A",
				"role_id": 2,
				"phone": "+56987654321"
				}
			}


# ==========================================
# RESPONSES - EMPLOYEE
# ==========================================

class EmployeeResponse(BaseModel):
	"""Información del empleado"""
	id: int
	full_name: str
	rut: str
	role_id: int
	user_id: Optional[int] = None
	active: bool
	phone: Optional[str] = None
	address: Optional[str] = None
	hire_date: Optional[datetime] = None
	created_at: Optional[datetime] = None

	class Config:
			from_attributes = True


class EmployeeListResponse(BaseModel):
	"""Respuesta con lista de empleados"""
	employees: list[EmployeeResponse]
	total: int

	class Config:
		json_schema_extra = {
			"example": {
				"employees": [
					{
						"id": 1,
						"full_name": "Juan Pérez",
						"rut": "12345678-K",
						"role_id": 1,
						"user_id": 1,
						"active": True,
						"phone": "+56912345678",
						"address": "Calle Principal 123"
					}
				],
				"total": 1
			}
		}


class DeleteResponse(BaseModel):
	"""Respuesta de eliminación exitosa"""
	message: str
	id: int

	class Config:
		json_schema_extra = {
			"example": {
				"message": "Registro eliminado exitosamente",
				"id": 1
			}
		}


class StatusUpdateResponse(BaseModel):
	"""Respuesta de cambio de estado"""
	message: str
	id: int
	active: bool

	class Config:
		json_schema_extra = {
			"example": {
				"message": "Estado actualizado",
				"id": 1,
				"active": False
			}
		}
