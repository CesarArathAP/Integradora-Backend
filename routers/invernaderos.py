from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from controllers.invernaderos_controller import (
    crear_invernadero,
    obtener_invernaderos,
    obtener_invernadero_por_id,
    actualizar_invernadero,
    eliminar_invernadero
)

router = APIRouter(prefix="/invernaderos", tags=["Invernaderos"])

# --- Schema ---
class InvernaderoSchema(BaseModel):
    id_lote: str
    nombre: str
    ubicacion: str
    responsable: Optional[str] = None
    fecha_registro: Optional[str] = None
    superficie_m2: Optional[float] = 0
    tipo_cultivo: Optional[str] = ""
    estado: Optional[str] = "Activo"
    etapas_principales: Optional[List[str]] = []
    etapa_actual: Optional[str] = ""

# --- Endpoints ---
@router.post("/")
def crear_invernadero_endpoint(data: InvernaderoSchema):
    return crear_invernadero(data.dict())

@router.get("/")
def listar_invernaderos():
    return {"invernaderos": obtener_invernaderos()}

@router.get("/{invernadero_id}")
def obtener_invernadero_endpoint(invernadero_id: str):
    return obtener_invernadero_por_id(invernadero_id)

@router.put("/{invernadero_id}")
def actualizar_invernadero_endpoint(invernadero_id: str, data: InvernaderoSchema):
    return actualizar_invernadero(invernadero_id, data.dict())

@router.delete("/{invernadero_id}")
def eliminar_invernadero_endpoint(invernadero_id: str):
    return eliminar_invernadero(invernadero_id)
