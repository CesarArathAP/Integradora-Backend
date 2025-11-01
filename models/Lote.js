// models/Lote.js
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

// --- Sub-Schemas para Actividades ---

const AuditoriaActividadSchema = new Schema({
    estado: { type: String, default: 'PENDIENTE', enum: ['APROBADO', 'ALERTA', 'PENDIENTE'] },
    motivo: { type: String, default: null },
    nota_auditor: { type: String, default: null }
}, { _id: false });

const EvidenciaSchema = new Schema({
    url: { type: String, required: true },
    descripcion: { type: String, default: '' }
}, { _id: false });

const DatosEtapaSchema = new Schema({
    nombre: { type: String, required: true },
    fecha_inicio: { type: Date, required: true },
    fecha_fin: { type: Date, default: null },
    descripcion: { type: String, default: '' },
    cantidad_cosechada: { type: Number, default: 0 },
    unidad_cosecha: { type: String, default: '' },
    responsable_id: { type: Schema.Types.ObjectId, ref: 'Usuario' }
}, { _id: false });

const DatosInsumoSchema = new Schema({
    nombre: { type: String, required: true },
    proveedor_id: { type: Schema.Types.ObjectId, ref: 'Proveedor' },
    lote_insumo_externo: { type: String, default: null },
    cantidad: { type: Number, required: true },
    unidad: { type: String, required: true },
    notas: { type: String, default: '' }
}, { _id: false });

const ActividadSchema = new Schema({
    actividad_id: { type: String, required: true, unique: true }, // 8c4d5e6f7892-001
    tipo_evento: { type: String, required: true, enum: ['ETAPA', 'INSUMO', 'LABOR'] },
    fecha_registro: { type: Date, default: Date.now },
    datos_etapa: DatosEtapaSchema, // Se usará si tipo_evento es 'ETAPA'
    datos_insumo: DatosInsumoSchema, // Se usará si tipo_evento es 'INSUMO'
    evidencias: { type: [EvidenciaSchema], default: [] },
    auditoria: AuditoriaActividadSchema
}, { _id: false });

// --- Schema Principal ---
const LoteSchema = new Schema({
    codigo_qr: { type: String, required: true, unique: true }, // LOTE-7890-CHL-P005
    productor_id: { type: Schema.Types.ObjectId, ref: 'Usuario', required: true },
    invernadero_id: { type: Schema.Types.ObjectId, ref: 'Invernadero', required: true },
    cultivo_id: { type: Schema.Types.ObjectId, ref: 'EtapaPlantilla', required: true }, // Asumo que esto referencia a la plantilla de etapas
    cultivo_nombre: { type: String, required: true },
    superficie_m2: { type: Number, required: true },
    fecha_inicio_ciclo: { type: Date, required: true },
    fecha_cosecha_est: { type: Date, default: null },
    estado_trazabilidad: { type: String, default: 'ACTIVO', enum: ['ACTIVO', 'ALERTA', 'FINALIZADO', 'INACTIVO'] },
    rendimiento_total_kg: { type: Number, default: 0 },
    actividades: { type: [ActividadSchema], default: [] }
}, {
    timestamps: true,
    collection: 'lotes'
});

module.exports = mongoose.model('Lote', LoteSchema);