# controllers/sincronizacion_controller.py
from fastapi import HTTPException
from database import db
from datetime import datetime

async def sincronizar_datos(modulo: str, data: dict):
    """
    Guarda los datos directamente en la colección de MongoDB
    según el módulo recibido.
    """
    colecciones_validas = {
        "etapas": db["etapas_produccion"],
        "insumos": db["insumos"],
        "invernaderos": db["invernaderos"],
        "lotes": db["lotes"],
        "usuarios": db["usuarios"]
    }

    # Verificar que el módulo sea válido
    if modulo not in colecciones_validas:
        raise HTTPException(status_code=400, detail=f"Módulo '{modulo}' no válido")

    coleccion = colecciones_validas[modulo]

    # Validar que data sea un diccionario
    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="El campo 'data' debe ser un diccionario")

    # Agregar marca de tiempo
    data["fecha_sincronizacion"] = datetime.now().isoformat()

    # Insertar en Mongo
    try:
        resultado = coleccion.insert_one(data)
        return {
            "mensaje": f"Registro insertado correctamente en '{modulo}'",
            "id_insertado": str(resultado.inserted_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar en MongoDB: {str(e)}")
