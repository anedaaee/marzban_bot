const userRouter = require('./routers/user')
const adminRouter = require('./routers/admin')
const managerRouter = require('./routers/manager')

const checkAdmin = require('./middleware/admin.check')
const checkManager = require('./middleware/manager.check')
const checkSpam = require('./middleware/spam.check')

exports.app_use = (app) => {
    app.use('/api/user' , userRouter)
    app.use('/api/admin' ,checkSpam,checkAdmin, adminRouter)
    app.use('/api/manager' ,checkSpam,checkManager, managerRouter)

}