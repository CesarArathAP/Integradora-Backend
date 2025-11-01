// models/Reporte.js
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const ReporteSchema = new Schema({
    usuario_id: { type: Schema.Types.ObjectId, ref: 'Usuario', required: true },
    nombre_reporte: { type: String, required: true },
    tipo_reporte: { type: String, required: true, enum: ['Consumo', 'Rendimiento', 'Auditoria', 'Inventario'] },
    fecha_generacion: { type: Date, default: Date.now },
    formato: { type: String, default: 'PDF' },
    filtros_aplicados: { type: Object, default: {} }, // Contiene la lógica de filtrado usada
    url_reporte: { type: String, default: "" } // URL donde se almacena el reporte final
}, {
    timestamps: true,
    collection: 'reportes'
});

module.exports = mongoose.model('Reporte', ReporteSchema);