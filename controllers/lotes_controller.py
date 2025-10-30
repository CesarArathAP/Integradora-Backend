from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime
from database import db

lotes_col = db["lotes"]

def _to_str(o):
    if isinstance(o, ObjectId):
        return str(o)
    elif isinstance(o, dict):
        return {k: _to_str(v) for k, v in o.items()}
    elif isinstance(o, list):
        return [_to_str(i) for i in o]
    else:
        return o

def crear_lote(data: dict):
    now = datetime.utcnow()
    doc = {
        "id_invernadero": data.get("id_invernadero"),
        "nombre_lote": data.get("nombre_lote"),
        "tipo_cultivo": data.get("tipo_cultivo"),
        "fecha_inicio": data.get("fecha_inicio") or now,
        "etapas": data.get("etapas", []),
        "estado": data.get("estado", "Activo")
    }
    result = lotes_col.insert_one(doc)
    return {"mensaje": "Lote registrado", "id": str(result.inserted_id)}

def obtener_lotes():
    return [_to_str(l) for l in lotes_col.find()]

def obtener_lote_por_id(id_lote: str):
    lote = lotes_col.find_one({"_id": ObjectId(id_lote)})
    if not lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    return _to_str(lote)

def actualizar_lote(id_lote: str, data: dict):
    result = lotes_col.update_one({"_id": ObjectId(id_lote)}, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    return {"mensaje": "Lote actualizado correctamente"}

def eliminar_lote(id_lote: str):
    result = lotes_col.delete_one({"_id": ObjectId(id_lote)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    return {"mensaje": "Lote eliminado correctamente"}
