from bson import ObjectId
from fastapi import HTTPException
from database import db

invernaderos_collection = db["invernaderos"]

# --- Helpers ---
def convert_objectid(obj):
    """
    Convierte recursivamente ObjectId a string dentro de diccionarios y listas.
    """
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, list):
        return [convert_objectid(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_objectid(v) for k, v in obj.items()}
    else:
        return obj

def _to_str(doc):
    """Convierte recursivamente ObjectId a str en todo el documento."""
    if isinstance(doc, list):
        return [_to_str(item) for item in doc]
    elif isinstance(doc, dict):
        new_doc = {}
        for k, v in doc.items():
            new_doc[k] = _to_str(v)
        return new_doc
    elif isinstance(doc, ObjectId):
        return str(doc)
    else:
        return doc

# --- Controladores ---
def crear_invernadero(data: dict):

    # Si quieres agregar automáticamente fecha_registro
    if "fecha_registro" not in data or not data["fecha_registro"]:
        from datetime import datetime
        data["fecha_registro"] = datetime.utcnow().isoformat()

    # Asegurar que ingenieros_asignados siempre sea lista
    if "ingenieros_asignados" not in data:
        data["ingenieros_asignados"] = []

    # Asegurar que etapas_principales siempre exista
    if "etapas_principales" not in data:
        data["etapas_principales"] = []

    # Asegurar que etapa_actual exista
    if "etapa_actual" not in data:
        data["etapa_actual"] = ""

    result = invernaderos_collection.insert_one(data)
    return {"mensaje": "Invernadero creado", "id": str(result.inserted_id)}


def obtener_invernaderos():
    return [_to_str(i) for i in invernaderos_collection.find()]

def obtener_invernadero_por_id(invernadero_id: str):
    invernadero = invernaderos_collection.find_one({"_id": ObjectId(invernadero_id)})
    if not invernadero:
        raise HTTPException(status_code=404, detail="Invernadero no encontrado")
    return _to_str(invernadero)

def obtener_invernadero_por_lote(id_lote: str):
    """
    Devuelve un invernadero buscado por id_lote en lugar del _id ObjectId.
    """
    invernadero = invernaderos_collection.find_one({"id_lote": id_lote})
    
    if not invernadero:
        raise HTTPException(status_code=404, detail="Invernadero no encontrado")
    
    return _to_str(invernadero)

def obtener_etapas_por_lote(id_lote: str):
    invernadero = invernaderos_collection.find_one(
        {"id_lote": id_lote},
        {"etapas_principales": 1, "_id": 0}  # ← Solo traer este campo
    )

    if not invernadero:
        raise HTTPException(status_code=404, detail="Invernadero no encontrado")

    return invernadero.get("etapas_principales", [])

def obtener_catalogo_etapas():
    cursor = invernaderos_collection.find({}, {"etapas_principales": 1})

    etapas_set = set()

    for doc in cursor:
        etapas = doc.get("etapas_principales", [])
        if isinstance(etapas, list):
            for e in etapas:
                etapas_set.add(e)

    # Convertir set → lista ordenada
    return sorted(list(etapas_set))

def actualizar_invernadero(invernadero_id: str, data: dict):
    if "responsable" in data and data["responsable"]:
        try:
            data["responsable"] = ObjectId(data["responsable"])
        except Exception:
            pass

    result = invernaderos_collection.update_one(
        {"_id": ObjectId(invernadero_id)}, {"$set": data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Invernadero no encontrado")
    return {"mensaje": "Invernadero actualizado correctamente"}

def eliminar_invernadero(invernadero_id: str):
    result = invernaderos_collection.delete_one({"_id": ObjectId(invernadero_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Invernadero no encontrado")
    return {"mensaje": "Invernadero eliminado correctamente"}
