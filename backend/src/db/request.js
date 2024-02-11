
function request(query, params , req) {
    return new Promise((resolve, reject) => {
        let pool;
        if(req.app.locals.db){
            pool = req.app.locals.db
        }else {
            pool = req
        }
        pool.getConnection((err, connection) => {
            if (err) {
                reject(err);
                return;
            }

            connection.query(query, params, (error, results) => {
                connection.release(); // Release the connection back to the pool
                if (error) {
                    reject(error);
                    return;
                }
                resolve(results);
            });
        });
    });
}

module.exports = request