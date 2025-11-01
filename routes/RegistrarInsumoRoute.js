// routes/RegistrarInsumoRoute.js
const express = require('express');
const router = express.Router();
const { registrarInsumo } = require('../controllers/RegistrarInsumo'); 

// Middleware para manejo de errores en rutas asíncronas
const asyncHandler = fn => (req, res, next) => 
    Promise.resolve(fn(req, res, next)).catch(err => {
        const status = err.status || 500;
        const detail = err.message || "Error interno del servidor";
        res.status(status).json({ detail });
    });

// POST /api/insumos/
router.post('/', asyncHandler(registrarInsumo));

module.exports = router;