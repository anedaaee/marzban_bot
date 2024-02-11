const Joi = require('joi')
const request = require('../db/request')

const checkManager = async(req,res,next) => {
    const schema = Joi.object({
        chat_id : Joi.string().required()
    }).unknown(true)
    
    const values = await schema.validateAsync(req.query)

    const query = `SELECT rule FROM KianDB.users WHERE chat_id =? ;`

    const rule = await request(query,[values.chat_id],req)
    if(rule.length != 0){
        if(rule[0].rule === 'manager'){
            next()
        }else{
            return res.status(401).send({
                "metadata": {
                    message : 'you dont have permission'
                }
            })
        }
    }else{
        return res.status(401).send({
            "metadata": {
                message : 'you dont have permission'
            }
        })
    }
}

module.exports = checkManager