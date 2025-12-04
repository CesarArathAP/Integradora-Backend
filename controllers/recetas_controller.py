from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime
from database import db   # tu conexión a MongoDB

recetas_collection = db["recetas_invernadero"]

# -------------------------------------------------------------------
# ✔ SERIALIZADOR COMPLETO (soluciona el error JSON Parse)
# -------------------------------------------------------------------
def serialize_mongo(doc):
    if isinstance(doc, list):
        return [serialize_mongo(item) for item in doc]

    if isinstance(doc, dict):
        new = {}
        for k, v in doc.items():

            # --- ObjectId ---
            if isinstance(v, ObjectId):
                new[k] = str(v)

            # --- datetime ---
            elif isinstance(v, datetime):
                new[k] = v.isoformat()

            # --- formato Mongo $date { $numberLong } ---
            elif isinstance(v, dict) and "$date" in v:
                try:
                    new[k] = int(v["$date"]["$numberLong"])
                except:
                    new[k] = v
            else:
                new[k] = serialize_mongo(v)
        return new

    return doc

# -------------------------------------------------------------------
# ✔ CONSULTAS
# -------------------------------------------------------------------

def obtener_recetas():
    """Retorna todas las recetas"""
    recetas = recetas_collection.find()
    return [serialize_mongo(r) for r in recetas]

def obtener_receta_por_id(receta_id: str):
    receta = recetas_collection.find_one({"_id": ObjectId(receta_id)})
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return serialize_mongo(receta)

def obtener_recetas_por_invernadero(id_invernadero: str):
    recetas = recetas_collection.find({"id_invernadero": id_invernadero})
    return [serialize_mongo(r) for r in recetas]

# -------------------------------------------------------------------
# ✔ ACTUALIZAR ESTADO
# -------------------------------------------------------------------
def actualizar_estado_receta(receta_id: str, nuevo_estado: str):
    receta = recetas_collection.find_one({"_id": ObjectId(receta_id)})

    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")

    # Actualizar solo el estado
    recetas_collection.update_one(
        {"_id": ObjectId(receta_id)},
        {"$set": {"estado": nuevo_estado}}
    )

    receta_actualizada = recetas_collection.find_one({"_id": ObjectId(receta_id)})
    return serialize_mongo(receta_actualizada)
