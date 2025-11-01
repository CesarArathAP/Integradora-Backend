// controllers/RegistrarInsumo.js
const Insumo = require('../models/Insumo');
const mongoose = require('mongoose');

const registrarInsumo = async (req, res) => {
    const data = req.body;
    
    // 1. Validación de campos obligatorios
    if (!data.codigo_interno || !data.nombre_comercial || !data.tipo_insumo || !data.unidad_inventario) {
        throw { status: 400, message: "Faltan campos obligatorios: codigo_interno, nombre_comercial, tipo_insumo y unidad_inventario." };
    }
    
    // 2. Mapeo de proveedor_id (Si existe, debe ser válido)
    if (data.proveedor_info && data.proveedor_info.proveedor_id) {
        const pId = data.proveedor_info.proveedor_id;
        if (!mongoose.Types.ObjectId.isValid(pId)) {
            throw { status: 400, message: "El proveedor_id proporcionado es inválido." };
        }
        data.proveedor_info.proveedor_id = new mongoose.Types.ObjectId(pId);
    }
    
    // NOTA: Si data.reglas_auditoria NO se proporciona, Mongoose usa los defaults (false, 0, "")
    // Por lo tanto, no se necesita lógica extra aquí.

    try {
        await Insumo.create(data); 
        
        res.status(201).json({ mensaje: "Insumo registrado correctamente" });
        
    } catch (error) {
        if (error.code === 11000) { 
            throw { status: 409, message: "El código interno del insumo ya está registrado." };
        }
        if (error.name === 'ValidationError') {
            throw { status: 400, message: error.message };
        }
        throw error; 
    }
};

module.exports = { registrarInsumo };