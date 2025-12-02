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
    """Crea una etapa EXACTA al formato de Mongo recibido desde la app."""

    doc = {
        "id_invernadero": data.get("id_invernadero"),
        "nombre_invernadero": data.get("nombre_invernadero"),
        "id_lote": data.get("id_lote"),
        "etapa_principal": data.get("etapa_principal"),
        "sub_etapa": data.get("sub_etapa"),

        # fechas y timestamp
        "fecha_aplicacion": data.get("fecha_aplicacion") or datetime.utcnow(),
        "fecha_sincronizacion": data.get("fecha_sincronizacion") or datetime.utcnow(),
        "timestamp": data.get("timestamp") or int(datetime.utcnow().timestamp() * 1000),

        "descripcion": data.get("descripcion", ""),
        "responsable": data.get("responsable", ""),
        "observaciones": data.get("observaciones", ""),

        # insumo aplicado como objeto
        "insumo_aplicado": data.get("insumo_aplicado", {}),

        # cosecha
        "cantidad_cosechada": data.get("cantidad_cosechada"),
        "unidad_cosecha": data.get("unidad_cosecha"),

        # evidencia (base64 o null)
        "evidencia": data.get("evidencia")
    }

    result = etapas.insert_one(doc)
    return {"mensaje": "Etapa registrada correctamente", "id": str(result.inserted_id)}

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
