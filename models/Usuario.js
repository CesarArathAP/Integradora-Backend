// models/Usuario.js
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const UsuarioSchema = new Schema({
    nombre_completo: { type: String, required: true },
    uid: { type: String, required: true, unique: true }, // P005, A001, etc.
    rol: { type: String, required: true, enum: ['Productor', 'Auditor', 'Administrador'] },
    email: { type: String, required: true, unique: true },
    password_hash: { type: String, required: true, select: false },
    estado: { type: String, required: true, default: 'Activo' },
    rfc: { type: String, default: null },
    telefono: { type: String, default: null }, 
    direccion: { type: String, default: null }, 
    fecha_registro: { type: Date, default: Date.now } // Campo explícito para la fecha de creación
}, {
    timestamps: false,     // <-- Desactiva createdAt y updatedAt
    versionKey: false,     // <-- Desactiva el campo __v
    collection: 'usuarios'
});

module.exports = mongoose.model('Usuario', UsuarioSchema);