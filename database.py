from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Usar certifi para el CA bundle en Windows/entornos con problemas TLS
try:
	import certifi
except Exception:
	certifi = None

# Carga las variables del .env
load_dotenv()

# Toma la URL de Mongo del .env
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")  # fallback a localhost

# Conexión al cluster: usar el CA bundle de certifi si está disponible.
if certifi:
	client = MongoClient(MONGO_URL, tls=True, tlsCAFile=certifi.where())
else:
	# Si certifi no está instalado, intenta conexión por defecto.
	# Si sigue fallando por TLS, instala certifi: pip install certifi
	client = MongoClient(MONGO_URL)

# Selección de base de datos
db = client["producto_trazabilidad"]
