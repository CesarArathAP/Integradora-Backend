// controllers/RegistrarUsuario.js
const Usuario = require('../models/Usuario');
const { hashPassword } = require('../utils/auth');

const registrarUsuario = async (req, res) => {
    const data = req.body;
    
    // 1. Validación de campos esenciales
    if (!data.nombre_completo || !data.email || !data.password_hash || !data.rol || !data.uid) {
        throw { status: 400, message: "Faltan campos obligatorios: nombre, email, password, rol, o uid." };
    }
    
    // 2. Hasheo de la contraseña
    const passwordTrunc = data.password_hash.substring(0, 72);
    data.password_hash = await hashPassword(passwordTrunc); 
    
    // 3. Creación del documento
    const doc = {
        nombre_completo: data.nombre_completo,
        uid: data.uid,
        rol: data.rol,
        email: data.email,
        password_hash: data.password_hash,
        estado: data.estado || 'Activo',
        rfc: data.rfc || null,
        telefono: data.telefono || null,
        direccion: data.direccion || null,
    };

    try {
        await Usuario.create(doc); // Ya no necesitamos guardar el resultado
        
        // --- RESPUESTA MODIFICADA AQUÍ ---
        res.status(201).json({ mensaje: "Usuario registrado correctamente" });
        
    } catch (error) {
        // Manejo de errores de duplicidad
        if (error.code === 11000) { 
            throw { status: 409, message: "El email o UID ya están registrados." };
        }
        throw error; 
    }
};

module.exports = { registrarUsuario };