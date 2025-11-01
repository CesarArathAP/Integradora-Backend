const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors'); 
const connectDB = require('./db/database'); 

const RegistrarRoute = require('./routes/RegistrarRoute');
const LoginRoute = require('./routes/LoginRoute');
const RegistrarInsumoRoute = require('./routes/RegistrarInsumoRoute');

const app = express();
const PORT = process.env.PORT || 3100;

connectDB();

app.use(cors()); 
app.use(express.json());
app.use(bodyParser.urlencoded({ extended: true })); 

app.get('/', (req, res) => {
    res.json({ mensaje: "API de AgroTech funcionando correctamente" });
});

app.use('/api/usuarios/registrar', RegistrarRoute);
app.use('/api/usuarios/login', LoginRoute);
app.use('/api/insumos/', RegistrarInsumoRoute);

app.use((req, res, next) => {
    res.status(404).json({ detail: `Ruta no encontrada: ${req.method} ${req.originalUrl}` });
});

app.use((err, req, res, next) => {
    const status = err.status || 500;
    const detail = err.message || "Error interno del servidor";
    
    if (status === 500) {
        console.error(err);
    }
    
    res.status(status).json({ detail });
});

app.listen(PORT, () => {
    console.log(`🚀 Servidor de AgroTech API corriendo en http://localhost:${PORT}`);
});