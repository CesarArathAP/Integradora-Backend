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
    id_productor: Optional[str] = None
    nombre: str
    ubicacion: str
    superficie_m2: Optional[float] = 0
    tipo_cultivo: Optional[str] = ""
    estado: Optional[str] = "Activo"

    latitud: Optional[str] = ""
    longitud: Optional[str] = ""

    ingenieros_asignados: Optional[List[str]] = []

    etapas_principales: Optional[List[str]] = []
    etapa_actual: Optional[str] = ""

    fecha_registro: Optional[str] = None

    __v: Optional[int] = 0

# --- Endpoints ---
@router.post("/")
def crear_invernadero_endpoint(data: InvernaderoSchema):
    return crear_invernadero(data.dict())

@router.get("/")
def listar_invernaderos_endpoint():
    return {"invernaderos": obtener_invernaderos()}

@router.get("/lote/{id_lote}")
def obtener_invernadero_por_lote_endpoint(id_lote: str):
    from controllers.invernaderos_controller import obtener_invernadero_por_lote
    return obtener_invernadero_por_lote(id_lote)


@router.get("/{invernadero_id}")
def obtener_invernadero_endpoint(invernadero_id: str):
    return obtener_invernadero_por_id(invernadero_id)

@router.put("/{invernadero_id}")
def actualizar_invernadero_endpoint(invernadero_id: str, data: InvernaderoSchema):
    return actualizar_invernadero(invernadero_id, data.dict())

@router.delete("/{invernadero_id}")
def eliminar_invernadero_endpoint(invernadero_id: str):
    return eliminar_invernadero(invernadero_id)
