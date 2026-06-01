
#---------------------
# Librerías
#---------------------
import hashlib
import bcrypt

#---------------------
# Inicio codigo
#---------------------

#---------------------
# Creación de hash
#---------------------
def hash_password(password: str) -> str:
	"""
	Hashea una contraseña usando SHA-256 + bcrypt
	Primero hace SHA-256 (siempre retorna 64 caracteres)
	Luego aplica bcrypt (permite cualquier tamaño)
	"""
	# Hash SHA-256 (siempre 64 chars = 64 bytes)
	sha256_hash = hashlib.sha256(password.encode()).hexdigest().encode()
	# Hashear con bcrypt (seguro porque SHA256 = 64 bytes < 72)
	# bcrypt_hash = pwd_context.hash(sha256_hash) -> no sirve error 72 max
	salt = bcrypt.gensalt(rounds=12)
	bcrypt_hash = bcrypt.hashpw(sha256_hash, salt)
	return bcrypt_hash


#---------------------
# Verificacion de contraseña
#---------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
	"""
	Verifica una contraseña contra su hash
	Debe hacer el mismo SHA-256 antes de comparar
	"""
	# Si hashed_password es bytes, decodificar a string
	if isinstance(hashed_password, bytes):
			hashed_password = hashed_password.decode('utf-8')

	sha256_hash = hashlib.sha256(plain_password.encode()).hexdigest().encode()
	if isinstance(hashed_password, str):
		hashed_password = hashed_password.encode('utf-8')

	return bcrypt.checkpw(sha256_hash, hashed_password)

#---------------------
# TESTEO
#---------------------

if __name__=="__main__":
	password1 = "MiPassword123!"
	hash1 = hash_password(password1)

	print(f"✅ Hash 1 OK: {hash1[:50]}...")
	print(f"✅ Verificación 1: {verify_password(password1, hash1)}")

	# Test 2: Contraseña LARGA (más de 72 caracteres)
	password2 = "Esta es una contraseña muy larga que supera los 72 bytes de límite que tiene bcrypt por razones de seguridad"
	hash2 = hash_password(password2)
	print(f"✅ Hash 2 OK: {hash2[:50]}...")
	print(f"✅ Verificación 2: {verify_password(password2, hash2)}")



