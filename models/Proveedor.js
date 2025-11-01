// models/Proveedor.js
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const ProveedorSchema = new Schema({
    nombre_comercial: { type: String, required: true, unique: true },
    uid: { type: String, required: true, unique: true }, // SP001
    tipo_producto: { type: [String], required: true },
    estado_operacional: { type: String, required: true, enum: ['Activo', 'Inactivo'], default: 'Activo' }
}, {
    timestamps: true,
    collection: 'proveedores'
});

module.exports = mongoose.model('Proveedor', ProveedorSchema);