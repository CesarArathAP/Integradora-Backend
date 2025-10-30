from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from controllers import lotes_controller

router = APIRouter(prefix="/lotes", tags=["Lotes"])

class LoteSchema(BaseModel):
    id_invernadero: str
    nombre_lote: str
    tipo_cultivo: str
    fecha_inicio: Optional[str] = None
    etapas: List[str] = []
    estado: Optional[str] = "Activo"

@router.post("/", summary="Crear un nuevo lote")
def crear_lote_endpoint(data: LoteSchema):
    return lotes_controller.crear_lote(data.dict())

@router.get("/", summary="Obtener todos los lotes")
def listar_lotes():
    return {"lotes": lotes_controller.obtener_lotes()}

@router.get("/{id_lote}", summary="Obtener lote por ID")
def obtener_lote(id_lote: str):
    return lotes_controller.obtener_lote_por_id(id_lote)

@router.put("/{id_lote}", summary="Actualizar un lote")
def actualizar_lote(id_lote: str, data: LoteSchema):
    return lotes_controller.actualizar_lote(id_lote, data.dict())

@router.delete("/{id_lote}", summary="Eliminar un lote")
def eliminar_lote(id_lote: str):
    return lotes_controller.eliminar_lote(id_lote)
