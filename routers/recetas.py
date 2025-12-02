from fastapi import APIRouter
from controllers.recetas_controller import (
    obtener_recetas,
    obtener_receta_por_id,
    obtener_recetas_por_invernadero,
    actualizar_estado_receta  # <-- nuevo import
)
from pydantic import BaseModel

router = APIRouter(prefix="/recetas", tags=["Recetas"])

# --- Esquema para actualizar estado ---
class EstadoUpdateSchema(BaseModel):
    nuevo_estado: str

@router.get("/")
def listar_recetas():
    """Retorna todas las recetas"""
    return {"recetas": obtener_recetas()}

@router.get("/{receta_id}")
def obtener_receta(receta_id: str):
    """Retorna una receta por su _id"""
    return obtener_receta_por_id(receta_id)

@router.get("/invernadero/{id_invernadero}")
def recetas_por_invernadero(id_invernadero: str):
    """Retorna todas las recetas de un invernadero específico"""
    return {"recetas": obtener_recetas_por_invernadero(id_invernadero)}

@router.patch("/estado/{receta_id}")
def cambiar_estado(receta_id: str, data: EstadoUpdateSchema):
    """Actualiza el estado de una receta validando contra el catálogo"""
    return actualizar_estado_receta(receta_id, data.nuevo_estado)
