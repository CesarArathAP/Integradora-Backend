// routes/LoginRoute.js
const express = require('express');
const router = express.Router();
const { loginUsuario } = require('../controllers/LoginUsuario'); 

// Middleware para manejo de errores en rutas asíncronas
const asyncHandler = fn => (req, res, next) => 
    Promise.resolve(fn(req, res, next)).catch(err => {
        const status = err.status || 500;
        const detail = err.message || "Error interno del servidor";
        res.status(status).json({ detail });
    });

// POST /
router.post('/', asyncHandler(loginUsuario));

module.exports = router;