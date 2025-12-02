from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import os

from controllers.reportes_controller import (
    crear_reporte,
    listar_reportes,
    obtener_pdf_path
)

router = APIRouter(prefix="/reportes", tags=["Reportes"])

# -------------------------
# Schema de entrada
# -------------------------
class ReporteSchema(BaseModel):
    titulo: str
    descripcion: Optional[str] = ""
    fecha_generacion: Optional[datetime] = None
    invernaderos: List[dict] = []
    etapas: List[dict] = []
    insumos: List[dict] = []
    pdf_path: Optional[str] = None  # RUTA DEL PDF


# -------------------------
# Endpoints
# -------------------------
@router.post("/", summary="Generar y guardar un reporte")
def crear_reporte_endpoint(data: ReporteSchema):
    return crear_reporte(data.dict())


@router.get("/", summary="Listar todos los reportes")
def listar_reportes_endpoint():
    return listar_reportes()


# -------------------------
# Descargar PDF por id
# -------------------------
@router.get("/pdf/{id}", summary="Descargar PDF del reporte")
def descargar_pdf(id: str):

    # Obtiene la ruta ABSOLUTA del PDF
    pdf_path = obtener_pdf_path(id)

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="El archivo PDF no existe")

    # --------- RESPUESTA CORRECTA ---------
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=os.path.basename(pdf_path)
    )
