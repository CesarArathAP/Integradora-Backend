from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any, Optional, List
from controllers.etapas_produccion_controller import (
    crear_etapa,
    obtener_etapas,
    obtener_etapas_por_id_lote,
    actualizar_etapa,
    cerrar_etapa,
    eliminar_etapa
)

router = APIRouter(prefix="/etapas", tags=["Etapas Producción"])

# --- Esquemas ---
class EtapaSchema(BaseModel):
    id_invernadero: str
    nombre_invernadero: str
    id_lote: str
    etapa_principal: str
    sub_etapa: str

    fecha_aplicacion: Optional[datetime] = None
    fecha_sincronizacion: Optional[datetime] = None
    timestamp: Optional[int] = None

    descripcion: Optional[str] = ""
    responsable: Optional[str] = ""
    observaciones: Optional[str] = ""

    insumo_aplicado: Dict[str, Any] = {}

    cantidad_cosechada: Optional[float] = None
    unidad_cosecha: Optional[str] = None

    evidencia: Optional[Any] = None


# --- Endpoints ---
@router.post("/", summary="Crear una nueva etapa")
def crear_etapa_endpoint(data: EtapaSchema):
    """
    Registra una nueva etapa de producción.
    """
    result = crear_etapa(data.dict())
    return result

@router.get("/", summary="Listar todas las etapas")
def listar_etapas():
    """
    Obtiene todas las etapas de producción.
    """
    lista = obtener_etapas()
    return {"etapas": lista}

@router.get("/{id_lote}", summary="Obtener etapas por ID de lote")
def obtener_etapas_por_lote_simple(id_lote: str):
    """
    Permite obtener las etapas usando directamente /etapas/{id_lote}
    Ejemplo:
      /etapas/INV-20251112-172919
    """
    etapas = obtener_etapas_por_id_lote(id_lote)
    return {"etapas": etapas}

@router.get("/lote/{id_lote}", summary="Listar etapas de un lote específico")
def etapas_por_lote(id_lote: str):
    """
    Obtiene las etapas de producción filtradas por id_lote.
    """
    etapas = obtener_etapas_por_id_lote(id_lote)
    return {"etapas": etapas}

@router.put("/{id}", summary="Actualizar una etapa")
def actualizar_etapa_endpoint(id: str, data: EtapaSchema):
    """
    Actualiza los datos de una etapa de producción.
    """
    result = actualizar_etapa(id, data.dict())
    return result

@router.delete("/{id}", summary="Eliminar una etapa")
def eliminar_etapa_endpoint(id: str):
    """
    Elimina una etapa de producción por su ID.
    """
    from controllers.etapas_produccion_controller import etapas
    from bson import ObjectId

    # Intenta usar ObjectId, si falla usa el string como está
    try:
        filtro = {"_id": ObjectId(id)}
    except Exception:
        filtro = {"_id": id}

    result = etapas.delete_one(filtro)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Etapa no encontrada")
    return {"mensaje": "Etapa eliminada correctamente"}
