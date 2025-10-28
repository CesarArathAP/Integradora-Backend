from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from controllers.etapas_produccion_controller import (
    crear_etapa,
    obtener_etapas,
    obtener_etapas_por_id_lote,
    actualizar_etapa,
    cerrar_etapa,
)

router = APIRouter(prefix="/etapas", tags=["Etapas Producción"])

# --- Esquemas ---
class EtapaSchema(BaseModel):
    id_lote: str
    etapa_principal: str
    nombre_sub_etapa: str
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    descripcion: Optional[str] = ""
    responsable: Optional[str] = None
    insumos_utilizados: List[dict] = []
    evidencias: List[dict] = []
    observaciones: Optional[str] = ""
    cantidad_cosechada: int = 0
    unidad_cosecha: Optional[str] = ""

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

@router.get("/lote/{id_lote}", summary="Listar etapas de un lote específico")
def etapas_por_lote(id_lote: str):
    """
    Obtiene las etapas de producción filtradas por id_lote.
    """
    etapas = obtener_etapas_por_id_lote(id_lote)
    return {"etapas": etapas}
