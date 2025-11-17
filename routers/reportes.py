from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from controllers.reportes_controller import crear_reporte, listar_reportes

router = APIRouter(prefix="/reportes", tags=["Reportes"])

# --- Schema ---
class ReporteSchema(BaseModel):
    titulo: str
    descripcion: Optional[str] = ""
    fecha_generacion: Optional[datetime] = None
    invernaderos: List[dict] = []
    etapas: List[dict] = []
    insumos: List[dict] = []

# --- Endpoints ---
@router.post("/", summary="Generar y guardar un reporte")
def crear_reporte_endpoint(data: ReporteSchema):
    return crear_reporte(data.dict())

@router.get("/", summary="Listar todos los reportes")
def listar_reportes_endpoint():
    return listar_reportes()
