from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from controllers.insumos_controller import (
    crear_insumo,
    obtener_insumos,
    obtener_insumo_por_id,
    actualizar_insumo,
    eliminar_insumo,
    descontar_stock,  # ya existente
    # 🔹 nueva función
    agregar_stock
)

router = APIRouter(prefix="/insumos", tags=["Insumos"])

# --- Schemas ---
class InsumoSchema(BaseModel):
    nombre: str
    tipo: str
    composicion: str                    # ⬅️ antes dict ⛔
    presentacion: str
    unidadMedida: str
    proveedor: str
    fechaCaducidad: str                 # ⬅️ antes datetime ⛔
    stock: Optional[float] = 0
    precioUnitario: str                 # ⬅️ antes float ⛔
    lotesAplicados: list = []
    observaciones: Optional[str] = None


class DescontarStockSchema(BaseModel):
    insumo_id: str
    cantidad_usada: float

# 🔹 Nuevo schema para agregar stock
class AgregarStockSchema(BaseModel):
    insumo_id: str
    cantidad_agregada: float

# --- Endpoints ---
@router.post("/")
def crear_insumo_endpoint(data: InsumoSchema):
    return crear_insumo(data.dict())

@router.get("/")
def listar_insumos():
    return {"insumos": obtener_insumos()}

@router.get("/invernadero/{id_lote}")
def obtener_insumos_por_lote(id_lote: str):
    from controllers.insumos_controller import obtener_insumos_por_invernadero
    return {"insumos": obtener_insumos_por_invernadero(id_lote)}

@router.get("/{insumo_id}")
def obtener_insumo(insumo_id: str):
    return obtener_insumo_por_id(insumo_id)

@router.put("/{insumo_id}")
def actualizar_insumo_endpoint(insumo_id: str, data: InsumoSchema):
    return actualizar_insumo(insumo_id, data.dict(exclude_unset=True))

@router.delete("/{insumo_id}")
def eliminar_insumo_endpoint(insumo_id: str):
    return eliminar_insumo(insumo_id)

# --- Endpoints de stock ---
@router.post("/descontar/")
def descontar_stock_endpoint(data: DescontarStockSchema):
    return descontar_stock(data.insumo_id, data.cantidad_usada)

@router.post("/agregar/")
def agregar_stock_endpoint(data: AgregarStockSchema):
    return agregar_stock(data.insumo_id, data.cantidad_agregada)
