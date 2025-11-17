# routers/sincronizacion.py
from fastapi import APIRouter, Body
from controllers.sincronizacion_controller import sincronizar_datos

router = APIRouter(prefix="/sincronizar", tags=["Sincronización"])

@router.post("/")
async def sincronizar(modulo: str = Body(...), data: dict = Body(...)):
    """
    Recibe los datos desde la app móvil y los guarda directamente
    en la colección Mongo correspondiente.
    """
    resultado = await sincronizar_datos(modulo, data)
    return resultado
