# Integradora-Backend

API REST para la gestión de trazabilidad agrícola, desarrollada con FastAPI y MongoDB.

## 🚀 Instalación rápida

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/Integradora-Backend.git
   cd Integradora-Backend
   ```

2. **Instala dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura variables de entorno**
   - Crea un archivo `.env` con tu cadena de conexión de MongoDB:
     ```
     MONGO_URL=mongodb+srv://usuario:contraseña@cluster.mongodb.net/db
     SECRET_KEY=tu_clave_secreta
     ```

4. **Ejecuta el servidor**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📚 Endpoints principales

- **Usuarios**
  - `POST /usuarios/login` — Login de usuario
  - `POST /usuarios/registrar` — Registrar usuario
  - `GET /usuarios/` — Listar usuarios

- **Lotes**
  - `POST /lotes/` — Crear lote
  - `GET /lotes/` — Listar lotes
  - `GET /lotes/{id_lote}` — Obtener lote por ID
  - `PUT /lotes/{id_lote}` — Actualizar lote
  - `DELETE /lotes/{id_lote}` — Eliminar lote

- **Etapas de Producción**
  - `POST /etapas/` — Crear etapa
  - `GET /etapas/` — Listar etapas
  - `GET /etapas/lote/{id_lote}` — Etapas por lote
  - `PUT /etapas/{id}` — Actualizar etapa
  - `DELETE /etapas/{id}` — Eliminar etapa

- **Insumos**
  - `POST /insumos/` — Crear insumo
  - `GET /insumos/` — Listar insumos
  - `GET /insumos/{id}` — Obtener insumo por ID
  - `PUT /insumos/{id}` — Actualizar insumo
  - `DELETE /insumos/{id}` — Eliminar insumo

## 🛠 Estructura del proyecto

```
controllers/      # Lógica de negocio y acceso a la base de datos
routers/          # Endpoints de la API
database.py       # Conexión a MongoDB
main.py           # Configuración principal de FastAPI
.env              # Variables de entorno
requirements.txt  # Dependencias Python
```

## 📝 Notas

- La documentación interactiva está disponible en [http://localhost:8000/docs](http://localhost:8000/docs)
- Permite CORS para pruebas con Expo y frontend móvil.
- Los IDs pueden ser ObjectId de MongoDB o personalizados según el modelo.

## 📧 Contacto

Para dudas o soporte, contacta a [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com)