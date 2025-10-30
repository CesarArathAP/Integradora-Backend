from bson import ObjectId
from fastapi import HTTPException
from database import db

invernaderos_collection = db["invernaderos"]

# --- Helpers ---
def _to_str(doc: dict):
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    if "responsable" in doc and isinstance(doc["responsable"], ObjectId):
        doc["responsable"] = str(doc["responsable"])
    return doc

# --- Controladores ---
def crear_invernadero(data: dict):
    # Convertir responsable a ObjectId si aplica
    if "responsable" in data and data["responsable"]:
        try:
            data["responsable"] = ObjectId(data["responsable"])
        except Exception:
            pass

    result = invernaderos_collection.insert_one(data)
    return {"mensaje": "Invernadero creado", "id": str(result.inserted_id)}

def obtener_invernaderos():
    return [_to_str(i) for i in invernaderos_collection.find()]

def obtener_invernadero_por_id(invernadero_id: str):
    invernadero = invernaderos_collection.find_one({"_id": ObjectId(invernadero_id)})
    if not invernadero:
        raise HTTPException(status_code=404, detail="Invernadero no encontrado")
    return _to_str(invernadero)

def actualizar_invernadero(invernadero_id: str, data: dict):
    # Convertir responsable a ObjectId si aplica
    if "responsable" in data and data["responsable"]:
        try:
            data["responsable"] = ObjectId(data["responsable"])
        except Exception:
            pass

    result = invernaderos_collection.update_one({"_id": ObjectId(invernadero_id)}, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Invernadero no encontrado")
    return {"mensaje": "Invernadero actualizado correctamente"}

def eliminar_invernadero(invernadero_id: str):
    result = invernaderos_collection.delete_one({"_id": ObjectId(invernadero_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Invernadero no encontrado")
    return {"mensaje": "Invernadero eliminado correctamente"}
