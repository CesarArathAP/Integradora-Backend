from fastapi import HTTPException
from datetime import datetime
from database import db
from bson import ObjectId, Binary
import os

# Colección MongoDB
reportes_col = db["reportes"]

# Carpeta donde se almacenan los PDFs locales
RUTA_REPORTES = os.path.join(os.path.dirname(__file__), "..", "reportes_pdfs")
os.makedirs(RUTA_REPORTES, exist_ok=True)

# -------------------------
# Helper: convert ObjectId a str
# -------------------------
def _to_str(doc):
    if isinstance(doc, list):
        return [_to_str(item) for item in doc]

    elif isinstance(doc, dict):
        new_dict = {}
        for k, v in doc.items():

            # Detectar PDFs o bytes
            if isinstance(v, (bytes, Binary)):
                new_dict[k] = "[BINARY DATA OMITIDO]"
                continue

            if isinstance(v, ObjectId):
                new_dict[k] = str(v)
                continue

            new_dict[k] = _to_str(v)

        return new_dict

    elif isinstance(doc, ObjectId):
        return str(doc)

    elif isinstance(doc, (bytes, Binary)):
        return "[BINARY DATA OMITIDO]"

    else:
        return doc

# -------------------------
# Crear reporte
# -------------------------
def crear_reporte(data: dict):
    # Fecha de generación si falta
    if "fecha_generacion" not in data or not data["fecha_generacion"]:
        data["fecha_generacion"] = datetime.utcnow()

    # Validar que no envíen PDF binario
    if "pdf" in data:
        raise HTTPException(
            status_code=400,
            detail="No se permite enviar el PDF directamente. Solo la ruta pdf_path o url_reporte."
        )

    # Si envían pdf_path local, aseguramos que sea absoluta
    if "pdf_path" in data and data["pdf_path"]:
        filename = os.path.basename(data["pdf_path"])
        data["pdf_path"] = os.path.join(RUTA_REPORTES, filename)

    # Si envían url_reporte, lo dejamos tal cual
    if "url_reporte" in data and data["url_reporte"]:
        data["url_reporte"] = data["url_reporte"]

    # Insertar en MongoDB
    result = reportes_col.insert_one(data)

    return {
        "mensaje": "Reporte guardado correctamente",
        "id": str(result.inserted_id)
    }

# -------------------------
# Listar reportes
# -------------------------
def listar_reportes():
    reportes = list(reportes_col.find())
    return {"reportes": [_to_str(r) for r in reportes]}

# -------------------------
# Obtener ruta PDF
# -------------------------
def obtener_pdf_path(id_reporte: str):
    reporte = reportes_col.find_one({"_id": ObjectId(id_reporte)})

    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    # Si tiene url externa, usarla directamente
    if "url_reporte" in reporte and reporte["url_reporte"]:
        return reporte["url_reporte"]

    # Si tiene pdf_path local
    if "pdf_path" in reporte and reporte["pdf_path"]:
        filename = os.path.basename(reporte["pdf_path"])
        ruta_final = os.path.join(RUTA_REPORTES, filename)
        if not os.path.exists(ruta_final):
            raise HTTPException(status_code=404, detail="El archivo PDF no existe")
        return ruta_final

    raise HTTPException(status_code=400, detail="Este reporte no tiene PDF asociado")
