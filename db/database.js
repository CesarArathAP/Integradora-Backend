// db/database.js
const mongoose = require('mongoose');

// Usamos la URL local temporal.
// El nombre de la base de datos se especifica en la URI: /trazabilidad_agrIcola
const dbURI = 'mongodb://localhost:27017/trazabilidad_agrIcola';

const connectDB = async () => {
  try {
    // La conexión de Mongoose maneja internamente las opciones modernas
    await mongoose.connect(dbURI); 
    console.log('Conectado exitosamente a la base de datos MongoDB');
  } catch (error) {
    console.error('Error al conectar a la base de datos MongoDB:', error);
    process.exit(1);
  }
};

module.exports = connectDB;