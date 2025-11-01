// models/Invernadero.js
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const InvernaderoSchema = new Schema({
    nombre: { type: String, required: true },
    uid: { type: String, required: true, unique: true }, // GHW001
    productor_id: { type: Schema.Types.ObjectId, ref: 'Usuario', required: true },
    ubicacion: { type: String, required: true },
    capacidad_m2: { type: Number, required: true },
    tipo_estructura: { type: String, required: true },
    estado_operacional: { type: String, default: 'Activo' },
    fecha_inicio_op: { type: Date, default: Date.now },
    notas: { type: String, default: "" },
    fecha_registro: { type: Date, default: Date.now }
}, {
    timestamps: true,
    collection: 'invernaderos'
});

module.exports = mongoose.model('Invernadero', InvernaderoSchema);