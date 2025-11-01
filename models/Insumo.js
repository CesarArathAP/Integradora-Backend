// models/Insumo.js
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const ReglasAuditoriaSchema = new Schema({
    requiere_auditoria: { type: Boolean, default: false },
    dosis_max_recomendada: { type: Number, default: 0 },
    unidad_dosis_max: { type: String, default: "" },
    dias_carencia: { type: Number, default: 0 }
}, { _id: false });

const ProveedorInfoSchema = new Schema({
    proveedor_id: { type: Schema.Types.ObjectId, ref: 'Proveedor' },
    nombre_proveedor: { type: String }
}, { _id: false });

const InsumoSchema = new Schema({
    codigo_interno: { type: String, required: true, unique: true }, // F-NPK-001
    nombre_comercial: { type: String, required: true },
    tipo_insumo: { type: String, required: true, enum: ['Fertilizante', 'Pesticida', 'Semilla', 'Otro'] },
    descripcion_tecnica: { type: String, default: "" },
    unidad_inventario: { type: String, required: true },
    stock_disponible_actual: { type: Number, default: 0 },
    estado_insumo: { type: String, default: 'Activo' },
    proveedor_info: ProveedorInfoSchema,
    reglas_auditoria: ReglasAuditoriaSchema,
    hoja_seguridad_url: { type: String, default: "" },
    fecha_alta: { type: Date, default: Date.now }
}, {
    timestamps: false,     // <-- CORREGIDO: Desactiva createdAt y updatedAt
    versionKey: false,     // <-- Desactiva el campo __v
    collection: 'insumos'
});

module.exports = mongoose.model('Insumo', InsumoSchema);