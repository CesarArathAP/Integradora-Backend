from bson import ObjectId
from fastapi import HTTPException
from database import db

insumos_collection = db["insumos"]

# --- Helpers ---
def _to_str(doc):
    """Convierte recursivamente ObjectId a str en todo el documento."""
    if isinstance(doc, list):
        return [_to_str(item) for item in doc]
    elif isinstance(doc, dict):
        return {k: _to_str(v) for k, v in doc.items()}
    elif isinstance(doc, ObjectId):
        return str(doc)
    else:
        return doc


def _filtro_id(id_value):
    """
    Devuelve un filtro seguro para MongoDB.
    Si es un ObjectId válido, lo usa.
    Si no, usa el string normal.
    """
    try:
        return {"_id": ObjectId(id_value)}
    except Exception:
        return {"_id": id_value}


# --- Controladores ---
def crear_insumo(data: dict):
    # Convertir campos a ObjectId si son válidos
    for key in ["id_invernadero", "id_etapa", "responsable"]:
        if key in data and data[key]:
            try:
                data[key] = ObjectId(data[key])
            except Exception:
                pass

    result = insumos_collection.insert_one(data)
    return {"mensaje": "Insumo creado", "id": str(result.inserted_id)}


def obtener_insumos():
    return [_to_str(i) for i in insumos_collection.find()]


def obtener_insumo_por_id(insumo_id: str):
    insumo = insumos_collection.find_one(_filtro_id(insumo_id))
    if not insumo:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    return _to_str(insumo)


def actualizar_insumo(insumo_id: str, data: dict):
    if "responsable" in data and data["responsable"]:
        try:
            data["responsable"] = ObjectId(data["responsable"])
        except Exception:
            pass

    result = insumos_collection.update_one(_filtro_id(insumo_id), {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    return {"mensaje": "Insumo actualizado correctamente"}


def eliminar_insumo(insumo_id: str):
    result = insumos_collection.delete_one(_filtro_id(insumo_id))
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    return {"mensaje": "Insumo eliminado correctamente"}


def descontar_stock(insumo_id: str, cantidad_usada: float):
    insumo = insumos_collection.find_one(_filtro_id(insumo_id))
    if not insumo:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")

    stock_actual = insumo.get("stock_disponible", 0)
    nuevo_stock = stock_actual - cantidad_usada

    if nuevo_stock < 0:
        raise HTTPException(status_code=400, detail="Stock insuficiente")

    insumos_collection.update_one(
        _filtro_id(insumo_id),
        {"$set": {"stock_disponible": nuevo_stock}}
    )

    return {
        "mensaje": "Stock actualizado correctamente",
        "nuevo_stock": nuevo_stock
    }


# --- NUEVA FUNCIÓN: obtener insumos por lote/invernadero ---
def obtener_insumos_por_invernadero(id_lote: str):
    """
    Devuelve todos los insumos cuyo id_invernadero coincida con id_lote.
    No intenta convertir a ObjectId porque id_lote es texto (ej: INV-2025...)
    """
    insumos = list(insumos_collection.find({"id_invernadero": id_lote}))
    return _to_str(insumos)
