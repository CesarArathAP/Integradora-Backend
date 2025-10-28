from fastapi import FastAPI
from routers import usuarios, etapas_produccion

app = FastAPI(title="AgroTech API", version="1.0")

app.include_router(usuarios.router)
app.include_router(etapas_produccion.router)

@app.get("/")
def root():
    return {"mensaje": "API de AgroTech funcionando correctamente"}
