from fastapi import HTTPException
from datetime import datetime
from database import db
from bson import ObjectId

# Colección MongoDB
reportes_col = db["reportes"]

# --- Helpers ---
def _to_str(doc):
    """Convierte ObjectId a str en todo el documento."""
    if isinstance(doc, list):
        return [_to_str(item) for item in doc]
    elif isinstance(doc, dict):
        return {k: _to_str(v) for k, v in doc.items()}
    elif isinstance(doc, ObjectId):
        return str(doc)
    else:
        return doc

# --- Controladores ---
def crear_reporte(data: dict):
    """
    Guarda un reporte completo en MongoDB.
    """
    if "fecha_generacion" not in data or not data["fecha_generacion"]:
        data["fecha_generacion"] = datetime.utcnow()

    result = reportes_col.insert_one(data)
    return {"mensaje": "Reporte generado correctamente", "id": str(result.inserted_id)}

def listar_reportes():
    """
    Lista todos los reportes guardados.
    """
    reportes = list(reportes_col.find())
    return {"reportes": [_to_str(r) for r in reportes]}
