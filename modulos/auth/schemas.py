from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# ==========================================
# REQUESTS (Lo que llega del cliente)
# ==========================================

class UserRegister(BaseModel):
	"""Datos para registrar un nuevo usuario"""
	email: EmailStr
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
