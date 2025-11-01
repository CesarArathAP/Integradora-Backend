// models/Auditoria.js
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const AdjuntoSchema = new Schema({
    tipo: { type: String },
    url: { type: String }
}, { _id: false });

const HistorialResolucionSchema = new Schema({
    accion: { type: String, required: true }, // EJ: SOLICITUD_DE_CORRECCIÓN, JUSTIFICACION_PRODUCTOR
    usuario_id: { type: Schema.Types.ObjectId, ref: 'Usuario', required: true },
    rol_usuario: { type: String },
    fecha: { type: Date, default: Date.now },
    nota: { type: String },
    adjuntos: { type: [AdjuntoSchema], default: [] }
}, { _id: false });

const AuditoriaSchema = new Schema({
    lote_id: { type: Schema.Types.ObjectId, ref: 'Lote', required: true },
    codigo_qr_lote: { type: String, required: true },
    actividad_id_origen: { type: String, required: true }, // ID de la actividad dentro del lote que generó la alerta
    tipo_alerta: { type: String, required: true }, // Sobredosis de Insumo, Falta de Registro, etc.
    gravedad: { type: String, required: true, enum: ['ALTA', 'MEDIA', 'BAJA'] },
    descripcion_alerta: { type: String, required: true },
    estado_alerta: { type: String, required: true, enum: ['ABIERTA', 'JUSTIFICADO', 'CERRADA', 'RECHAZADA'] },
    auditor_asignado_id: { type: Schema.Types.ObjectId, ref: 'Usuario', default: null },
    fecha_creacion: { type: Date, default: Date.now },
    fecha_ultima_actualizacion: { type: Date, default: Date.now },
    historial_resolucion: { type: [HistorialResolucionSchema], default: [] }
}, {
    timestamps: true,
    collection: 'auditorias'
});

module.exports = mongoose.model('Auditoria', AuditoriaSchema);