const express = require('express')
const Joi = require('joi')
const userCtrl = require('../controller/user.ctrl')
const router = new express.Router()

router.get('/check-user', async(req,res) => {
    try{    
        const schema = Joi.object({
            chat_id : Joi.string().required()
        })

        const values = await schema.validateAsync(req.query)

        const users = await userCtrl.checkUser(values,req)

        if(users.length === 0){
            res.status(401).send({
                "metadata": {
                    message : 'user not found please signup first'
                },
            })
        }else{
            res.status(200).send({
                "metadata": {
                    message : 'every thing is okay'
                },
                "body": {
                    "type": "object",
                    "data": users[0]
                }
            })
        }

    }catch(err){
        console.log(err);
        let message = 'error happend bad request'
        
        if (err.details){
            message = 'invalid input'
        }

        return res.status(400).send({
            "metadata": {
                message : message
            }
        })
    }
}) 


router.post('/new-user', async(req,res) => {
    try{    
        const schema = Joi.object({
            chat_id : Joi.string().required(),
            name : Joi.string().required(),
            username : Joi.string().required(),
            phone : Joi.string().required(),
            config_name : Joi.string().optional(),
        })

        const values = await schema.validateAsync(req.body)

        await userCtrl.newUser(values,req)

        res.status(200).send({
            "metadata": {
                message : 'every thing is okay'
            },
        })

    }catch(err){
        console.log(err);
        let message = 'error happend bad request'
        
        if (err.details){
            message = 'invalid input'
        }

        return res.status(400).send({
            "metadata": {
                message : message
            }
        })
    }
}) 


router.get('/get-configs', async(req,res) => {
    try{    
        const schema = Joi.object({
            chat_id : Joi.string().required()
        })

        const values = await schema.validateAsync(req.query)

        const templates = await userCtrl.getConfigs(values,req)

        res.status(200).send({
            "metadata": {
                message : 'every thing is okay'
            },
            "body": {
                "type": "array",
                "data": templates
            }
        })

    }catch(err){
        let message = 'error happend bad request'
        
        if (err.details){
            message = 'invalid input'
        }

        return res.status(400).send({
            "metadata": {
                message : message
            }
        })
    }
}) 

router.get('/get-config', async(req,res) => {
    try{    
        const schema = Joi.object({
            template_id : Joi.number().required()
        })

        const values = await schema.validateAsync(req.query)

        const template = await userCtrl.getTemplate(values,req)
        
        res.status(200).send({
            "metadata": {
                message : 'every thing is okay'
            },
            "body": {
                "type": "object",
                "data": template[0]
            }
        })

    }catch(err){
        console.log(err);
        let message = 'error happend bad request'
        
        if (err.details){
            message = 'invalid input'
        }

        return res.status(400).send({
            "metadata": {
                message : message
            }
        })
    }
}) 

router.post('/purchase', async(req,res) => {
    try{    
        const schema = Joi.object({
            chat_id : Joi.string().required(),
            template_id : Joi.number().required(),
            name : Joi.string().required()
        })

        const values = await schema.validateAsync(req.body)

        const config = await userCtrl.purchase(values,req)
        console.log(config.data);
 
        res.status(200).send({
            "metadata": {
                "message" : 'every thing is okay'
            },
            "body": {
                "type": "object",
                "data": {
                    "config" : {
                        "expire": config.data.status == 'on_hold' && ! config.data.expire?  'not started yet' : config.data.expire,
                        "data_limit": config.data.data_limit,
                        "name":config.data.username,
                        "status":config.data.status,
                        "subscription_url":config.data.subscription_url
                    }
                }
            }
        })

    }catch(err){
        console.log(err); 
        let message = 'error happend bad request'
        
        if (err.details){
            message = 'invalid input'
        }

        return res.status(400).send({
            "metadata": {
                message : message
            }
        })
    }
}) 



router.get('/get-account-debt-history', async(req,res) => {
    try{    
        const schema = Joi.object({
            chat_id : Joi.string().required()
        })

        const values = await schema.validateAsync(req.query)

        const history = await userCtrl.getAccountDebt_history(values,req)

        res.status(200).send({
            "metadata": {
                message : 'every thing is okay'
            },
            "body": {
                "type": "array",
                "data": history
            }
        })

    }catch(err){
        let message = 'error happend bad request'
        
        if (err.details){
            message = 'invalid input'
        }

        return res.status(400).send({
            "metadata": {
                message : message
            }
        })
    }
}) 

router.get('/get-config-link', async(req,res) => {
    try{    
        const schema = Joi.object({
            id : Joi.number().required()
        })

        const values = await schema.validateAsync(req.query)

        const configLink = await userCtrl.getConfigLink(values,req)

        res.status(200).send({
            "metadata": {
                message : 'every thing is okay'
            },
            "body": {
                "type": "array",
                "data": configLink
            }
        }) 

    }catch(err){
        console.log(err);
        let message = 'error happend bad request'
        
        if (err.details){
            message = 'invalid input'
        }

        return res.status(400).send({
            "metadata": {
                message : message
            }
        })
    }
}) 

module.exports = router