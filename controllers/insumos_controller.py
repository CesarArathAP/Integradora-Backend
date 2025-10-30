from bson import ObjectId
from fastapi import HTTPException
from database import db

insumos_collection = db["insumos"]

# --- Helpers ---
def _to_str(doc: dict):
    doc = dict(doc)  # copia para no modificar el original
    for k, v in doc.items():
        if isinstance(v, ObjectId):
            doc[k] = str(v)
    return doc

# --- Controladores ---
def crear_insumo(data: dict):
    # Convertir IDs a ObjectId si es necesario
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
    insumo = insumos_collection.find_one({"_id": ObjectId(insumo_id)})
    if not insumo:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    return _to_str(insumo)

def actualizar_insumo(insumo_id: str, data: dict):
    # Convertir responsable a ObjectId si aplica
    if "responsable" in data and data["responsable"]:
        try:
            data["responsable"] = ObjectId(data["responsable"])
        except Exception:
            pass

    result = insumos_collection.update_one({"_id": ObjectId(insumo_id)}, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    return {"mensaje": "Insumo actualizado correctamente"}

def eliminar_insumo(insumo_id: str):
    result = insumos_collection.delete_one({"_id": ObjectId(insumo_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    return {"mensaje": "Insumo eliminado correctamente"}
