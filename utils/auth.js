// utils/auth.js
const bcrypt = require('bcryptjs'); 
const saltRounds = 10; 

const hashPassword = async (password) => {
    return bcrypt.hash(password, saltRounds); 
};

const verifyPassword = async (password, hash) => {
    return bcrypt.compare(password, hash);
};

module.exports = {
    hashPassword,
    verifyPassword
};