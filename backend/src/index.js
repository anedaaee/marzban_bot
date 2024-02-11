require('dotenv').config()
const express = require('express')
// const path = require('path')
// const fs = require('fs')
const cors = require('cors')
// const morgan = require('morgan')
const cookieParser = require('cookie-parser')
const bodyParser = require('body-parser')
const helmet = require("helmet")
const pool = require('./db/mysql.js')
const routerUse = require('./routeUse.js');

const port = process.env.PORT

const app = express()


app.use(express.json())
app.use(helmet())
app.use(cors())
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))
app.use(cookieParser())

routerUse.app_use(app)

// Error handeling
app.use((err, req, res, next) => {
    if (err) {
        console.log(err);
        let message = 'Initial 500 error'
        if (!err.statusCode) { err.statusCode = 500 }
        return res.status(err.statusCode).send({
           "metadata": message
        })
    }
  
    next()
})

// 404 handeling
app.use((req, res) => {
    let message = 'route not found'
    res.status(404).send(message)
})


//create server
app.listen(port , () => {
    app.locals.db = pool
    console.log(`Server is up on port ${port}`)
})