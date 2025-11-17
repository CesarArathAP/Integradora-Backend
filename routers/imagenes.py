from fastapi import APIRouter
from pydantic import BaseModel
from controllers.imagenes_controller import subir_imagen_controller
from datetime import datetime

router = APIRouter(prefix="/imagenes", tags=["Imagenes"])

class ImagenSchema(BaseModel):
    id_invernadero: str
    id_etapa: str
    tipo: str
    nombre_original: str
    descripcion: str
    fecha_subida: datetime
    subido_por: str
    archivo_base64: str

@router.post("/")
def subir_imagen_endpoint(data: ImagenSchema):
    return subir_imagen_controller(data.dict())
