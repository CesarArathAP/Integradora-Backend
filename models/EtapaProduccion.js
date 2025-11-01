// models/EtapaProduccion.js
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const EtapaProduccionSchema = new Schema({
    id_lote: { type: String, required: true },
    etapa_principal: { type: String, required: true },
    nombre_sub_etapa: { type: String, required: true },
    fecha_inicio: { type: Date, default: Date.now },
    fecha_fin: { type: Date, default: null },
    descripcion: { type: String, default: "" },
    // El responsable es un String o un ObjectId, lo definimos flexible por ahora
    responsable: { type: Schema.Types.Mixed, default: null }, 
    insumos_utilizados: { type: [Object], default: [] },
    evidencias: { type: [Object], default: [] },
    observaciones: { type: String, default: "" },
    cantidad_cosechada: { type: Number, default: 0 },
    unidad_cosecha: { type: String, default: "" }
}, {
    // Configuración para que el JSON devuelva 'id' en lugar de '_id' (aunque el controlador usa _id)
    toJSON: { virtuals: true }, 
});

// El modelo se llamará 'etapas_produccion' en MongoDB
const EtapaProduccion = mongoose.model('EtapaProduccion', EtapaProduccionSchema); 

module.exports = EtapaProduccion;