from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime
from database import db

etapas = db["etapas_produccion"]


def _to_str(o):
    """Convierte ObjectId a str en todo el documento, incluyendo listas y dicts anidados."""
    if isinstance(o, ObjectId):
        return str(o)
    elif isinstance(o, dict):
        return {k: _to_str(v) for k, v in o.items()}
    elif isinstance(o, list):
        return [_to_str(i) for i in o]
    else:
        return o


def crear_etapa(data: dict):
    # Acepta campos nuevos y aplica defaults
    now = datetime.utcnow()
    doc = {}
    doc["id_lote"] = data.get("id_lote")
    doc["etapa_principal"] = data.get("etapa_principal")
    doc["nombre_sub_etapa"] = data.get("nombre_sub_etapa")
    # permitir que el cliente envíe fechas; si no vienen, usar now
    doc["fecha_inicio"] = data.get("fecha_inicio") or now
    doc["fecha_fin"] = data.get("fecha_fin")
    doc["descripcion"] = data.get("descripcion", "")
    # responsable puede ser id string; convertir a ObjectId si es válido
    responsable = data.get("responsable")
    if responsable:
        try:
            doc["responsable"] = ObjectId(responsable)
        except Exception:
            # si no es un ObjectId válido, guardarlo tal cual
            doc["responsable"] = responsable
    else:
        doc["responsable"] = None

    doc["insumos_utilizados"] = data.get("insumos_utilizados", [])
    doc["evidencias"] = data.get("evidencias", [])
    doc["observaciones"] = data.get("observaciones", "")
    doc["cantidad_cosechada"] = data.get("cantidad_cosechada", 0)
    doc["unidad_cosecha"] = data.get("unidad_cosecha", "")

    result = etapas.insert_one(doc)
    return {"mensaje": "Etapa registrada", "id": str(result.inserted_id)}


def obtener_etapas():
    lista = []
    for e in etapas.find():
        lista.append(_to_str(e))
    return lista


def obtener_etapas_por_id_lote(id_lote: str):
    lista = []
    for e in etapas.find({"id_lote": id_lote}):
        lista.append(_to_str(e))
    return lista


def actualizar_etapa(id: str, data: dict):
    # Si se intenta actualizar el responsable, convertir a ObjectId si aplica
    if "responsable" in data and data["responsable"]:
        try:
            data["responsable"] = ObjectId(data["responsable"])  # type: ignore
        except Exception:
            pass

    # Detecta si el id es un ObjectId válido
    try:
        filtro = {"_id": ObjectId(id)}
    except Exception:
        filtro = {"_id": id}

    result = etapas.update_one(filtro, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Etapa no encontrada")
    return {"mensaje": "Etapa actualizada correctamente"}


def cerrar_etapa(id: str):
    result = etapas.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"fecha_fin": datetime.utcnow()}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Etapa no encontrada")
    return {"mensaje": "Etapa cerrada correctamente"}

def eliminar_etapa(id: str):
    # Intenta usar ObjectId, si falla usa el string
    try:
        filtro = {"_id": ObjectId(id)}
    except Exception:
        filtro = {"_id": id}
    result = etapas.delete_one(filtro)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Etapa no encontrada")
    return {"mensaje": "Etapa eliminada correctamente"}
