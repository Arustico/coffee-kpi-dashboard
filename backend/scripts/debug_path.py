# backend/debug_paths.py
import os
import sys
from pathlib import Path

print("=== DEBUG DE PATHS ===")
print(f"ACTUAL DIR DE TRABAJO: {os.getcwd()}")
print("-"*50)
print(f"LOCACIÓN SCRIPT: {Path(__file__).parent}")
print("-"*50)
print(f"Python path: {sys.path}")
print("-"*50)
print(f"__file__: {__file__}")
print("="*50)

# Busca archivos comunes que podrían tener paths
for root, dirs, files in os.walk('.'):
	for file in files:
		if file.endswith(('.py', '.toml', '.env', '.json', '.yaml', '.yml')):
			filepath = Path(root) / file
			try:
				with open(filepath, 'r') as f:
					content = f.read()
					# Busca paths sospechosos
				if '../' in content or any(p in content for p in ['/home', '/Users', 'C:\\']):
					print(f" - Posible path en: {filepath}")
			except:
				pass
