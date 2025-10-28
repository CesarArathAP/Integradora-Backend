from fastapi import HTTPException
from passlib.context import CryptContext
from bson import ObjectId
from datetime import datetime
from database import db

usuarios = db["usuarios"]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def login_usuario(correo: str, password: str):
    usuario = usuarios.find_one({"correo": correo})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Truncar la contraseña a 72 caracteres para bcrypt
    password_trunc = password[:72]
    if not pwd_context.verify(password_trunc, usuario["password_hash"]):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return {
        "id": str(usuario["_id"]),
        "nombre": usuario["nombre"],
        "rol": usuario["rol"],
        "estado": usuario["estado"]
    }

def registrar_usuario(data: dict):
    data["fecha_registro"] = datetime.utcnow()
    # Truncar la contraseña a 72 caracteres para bcrypt
    password_trunc = data["password_hash"][:72]
    data["password_hash"] = pwd_context.hash(password_trunc)
    result = usuarios.insert_one(data)
    return {"mensaje": "Usuario registrado", "id": str(result.inserted_id)}
