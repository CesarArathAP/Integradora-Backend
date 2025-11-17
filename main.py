from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import sincronizacion, usuarios, etapas_produccion, insumos, invernaderos, lotes, imagenes, reportes

app = FastAPI(title="Sistema Integral de Trazabilidad Agricola", version="1.0")

# --- 🔓 Permitir peticiones desde cualquier origen (ideal para pruebas con Expo) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción puedes restringirlo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(usuarios.router)
app.include_router(etapas_produccion.router)
app.include_router(insumos.router)
app.include_router(invernaderos.router)
app.include_router(lotes.router)
app.include_router(sincronizacion.router)
app.include_router(imagenes.router)
app.include_router(reportes.router)
@app.get("/")
def root():
    return {"mensaje": "API de Sistema de trazabilidad agricola funcionando correctamente"}
