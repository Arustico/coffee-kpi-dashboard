from datetime import datetime, timedelta
from jose import JWTError, jwt
from os import getenv

SECRET_KEY = getenv("JWT_SECRET_KEY")
ALGORITHM = getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("JWT_EXPIRATION_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(getenv("JWT_REFRESH_EXPIRATION_DAYS", 7))

def create_access_token(data: dict) -> str:
	"""Crea un token de acceso JWT (Json Web Token) """
	to_encode = data.copy()
	expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt

def create_refresh_token(data: dict) -> str:
	"""Crea un JWT refresh token (válido más tiempo)"""
	to_encode = data.copy()
	expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt

def verify_token(token: str) -> dict:
	"""Verifica y decodifica un JWT"""
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		return payload
	except JWTError:
		return None
