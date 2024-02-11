const sql = require('mysql2')

const config = {
    host: process.env.DB_HOST,
    port: process.env.DB_PORT,
    user: process.env.DB_USER,
    password: process.env.DB_PWD,
    database: process.env.DB_NAME
};
console.log("start connection to databases");
const pool = sql.createPool(config);
console.log("databass connected");
module.exports = pool