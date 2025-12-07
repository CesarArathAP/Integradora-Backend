from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from controllers.usuarios_controller import login_usuario, registrar_usuario, usuarios as usuarios_collection

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# --- Esquemas ---
class LoginSchema(BaseModel):
    correo: str
    password: str

class UsuarioSchema(BaseModel):
    nombre: str
    correo: str
    password: str
    rol: str
    estado: str


# --- Endpoints ---
@router.post("/login", summary="Login de usuario")
def login(data: LoginSchema):
    """
    Permite iniciar sesión con correo y contraseña.
    """
    try:
        user = login_usuario(data.correo, data.password)
        return {"usuario": user, "mensaje": "Login exitoso"}
    except HTTPException as e:
        raise e

@router.post("/registrar", summary="Registrar nuevo usuario")
def registrar_usuario_endpoint(data: UsuarioSchema):
    """
    Crea un nuevo usuario en la base de datos.
    """
    return registrar_usuario(data.dict())

@router.get("/", summary="Obtener todos los usuarios")
def obtener_usuarios():
    """
    Devuelve la lista de todos los usuarios.
    """
    lista = list(usuarios_collection.find())
    for u in lista:
        u["_id"] = str(u["_id"])
    return {"usuarios": lista}
