// controllers/LoginUsuario.js
const Usuario = require('../models/Usuario');
const { verifyPassword } = require('../utils/auth'); 

const loginUsuario = async (req, res) => {
    const { correo, password } = req.body;
    
    if (!correo || !password) {
        throw { status: 400, message: "Correo y password son requeridos" }; 
    }
    
    const usuario = await Usuario.findOne({ email: correo }).select('+password_hash'); 
    
    if (!usuario) {
        throw { status: 404, message: "Usuario no encontrado" }; 
    }

    const passwordTrunc = password.substring(0, 72);
    const isMatch = await verifyPassword(passwordTrunc, usuario.password_hash);
    
    if (!isMatch) { 
        throw { status: 401, message: "Contraseña incorrecta" };
    }
    
    const userData = {
        id: usuario._id.toString(),
        nombre: usuario.nombre_completo, 
        rol: usuario.rol,
        estado: usuario.estado,
        uid: usuario.uid
    };
    
    res.json({ usuario: userData, mensaje: "Login exitoso" });
};

module.exports = { loginUsuario };