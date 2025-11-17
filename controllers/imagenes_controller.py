from fastapi import HTTPException
from datetime import datetime
import base64
import os
import uuid
from database import db  # Tu conexión a MongoDB

# Carpeta donde se guardarán las fotos
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

imagenes_collection = db["evidencias"]

def subir_imagen_controller(data: dict):
    try:
        # Validaciones mínimas
        required_fields = ["id_invernadero", "id_etapa", "tipo", "nombre_original", "descripcion", "fecha_subida", "subido_por", "archivo_base64"]
        for field in required_fields:
            if field not in data:
                raise HTTPException(status_code=400, detail=f"Falta el campo {field}")

        # Generar nombre único
        file_name = f"{uuid.uuid4().hex}_{data['nombre_original']}"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        # Guardar archivo en disco
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(data["archivo_base64"]))

        # URL relativa para guardar en DB
        url_archivo = f"/{UPLOAD_DIR}/{file_name}"

        # Crear registro
        registro = {
            "_id": str(uuid.uuid4().hex),
            "id_invernadero": data["id_invernadero"],
            "id_etapa": data["id_etapa"],
            "tipo": data["tipo"],
            "url_archivo": url_archivo,
            "nombre_original": data["nombre_original"],
            "descripcion": data["descripcion"],
            "fecha_subida": data["fecha_subida"],
            "subido_por": data["subido_por"],
        }

        # Guardar en MongoDB
        imagenes_collection.insert_one(registro)

        return {"success": True, "data": registro}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
