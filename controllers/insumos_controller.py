from bson import ObjectId
from fastapi import HTTPException
from database import db

insumos_collection = db["insumos"]

# --- Helpers ---

def _to_str(doc):
    if isinstance(doc, list):
        return [_to_str(item) for item in doc]
    elif isinstance(doc, dict):
        return {k: _to_str(v) for k, v in doc.items()}
    elif isinstance(doc, ObjectId):
        return str(doc)
    else:
        return doc

def _filtro_id(id_value):
    try:
        return {"_id": ObjectId(id_value)}
    except Exception:
        return {"_id": id_value}

# --- Controladores ---

def crear_insumo(data: dict):

    # Normalizar "compocision"
    if "compocision" in data:
        data["composicion"] = data.pop("compocision")

    normalizado = {}

    mapping = {
        "presentacion": "presentacion ",
        "proveedor": "proveedor ",
        "fechaCaducidad": "fecha de caducidad",
        "precioUnitario": "precio unitario",
        "unidadMedida": "unidadMedida",
        "lotesAplicados": "lotesAplicados",
        "nombre": "nombre",
        "tipo": "tipo",
        "composicion": "composicion",
        "stock": "stock",
        "stock_disponible": "stock_disponible",
    }

    # Normalizar nombres
    for k, v in data.items():
        if k in mapping:
            normalizado[mapping[k]] = v

    # Convertir stock
    try:
        normalizado["stock"] = float(normalizado.get("stock", 0))
    except:
        normalizado["stock"] = 0

    # Convertir precio
    if "precio unitario" in normalizado:
        try:
            p = normalizado["precio unitario"]
            p = p.replace("$", "").replace(".", "").replace(",", ".")
            normalizado["precio unitario"] = float(p)
        except:
            normalizado["precio unitario"] = 0

    result = insumos_collection.insert_one(normalizado)

    return {
        "mensaje": "Insumo creado",
        "id": str(result.inserted_id)
    }

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

    # Corregir typo si viene
    if "compocision" in data:
        data["composicion"] = data.pop("compocision")

    result = insumos_collection.update_one(
        _filtro_id(insumo_id),
        {"$set": data}
    )

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

    stock_actual = insumo.get("stock", 0)
    try:
        stock_actual = float(stock_actual)
        cantidad_usada = float(cantidad_usada)
    except:
        raise HTTPException(status_code=400, detail="Valores inválidos")

    nuevo_stock = stock_actual - cantidad_usada
    if nuevo_stock < 0:
        raise HTTPException(status_code=400, detail="Stock insuficiente")

    insumos_collection.update_one(
        _filtro_id(insumo_id),
        {"$set": {"stock": nuevo_stock}}
    )

    return {"mensaje": "Stock actualizado correctamente", "nuevo_stock": nuevo_stock}

def agregar_stock(insumo_id: str, cantidad_agregada: float):
    insumo = insumos_collection.find_one(_filtro_id(insumo_id))
    if not insumo:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")

    stock_actual = insumo.get("stock", 0)
    try:
        stock_actual = float(stock_actual)
        cantidad_agregada = float(cantidad_agregada)
    except:
        raise HTTPException(status_code=400, detail="Valores inválidos")

    nuevo_stock = stock_actual + cantidad_agregada

    insumos_collection.update_one(
        _filtro_id(insumo_id),
        {"$set": {"stock": nuevo_stock}}
    )

    return {"mensaje": "Stock agregado correctamente", "nuevo_stock": nuevo_stock}

# --- Obtener insumos por invernadero/lote ---

def obtener_insumos_por_invernadero(id_lote: str):
    insumos = list(insumos_collection.find({"id_invernadero": id_lote}))
    return _to_str(insumos)