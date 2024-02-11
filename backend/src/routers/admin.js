const express = require('express')
const Joi = require('joi')
const adminCtrl = require('../controller/admin.ctrl')
const router = new express.Router()

router.get('/get_users', async(req,res) => {
    try{    
        const schema = Joi.object({
            chat_id : Joi.string().required()
        })

        const values = await schema.validateAsync(req.query)

        const users = await adminCtrl.getUsers(values,req)

        res.status(200).send({
            "metadata": {
                message : 'every thing is okay'
            },
            "body": {
                "type": "array",
                "data": users
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

router.post('/add-template', async(req,res) => {
    try{    
        const schema = Joi.object({
            chat_id : Joi.string().required()
        })

        const chat_id = await schema.validateAsync(req.query)

        const valueSchema = Joi.object({
            template_id : Joi.number().required(),
            new_price : Joi.number().required()
        })

        const values = await valueSchema.validateAsync(req.body)

        await adminCtrl.addTemplate(chat_id,values,req)

        res.status(200).send({
            "metadata": {
                message : 'every thing is okay'
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

router.get('/get-admin-templates', async(req,res) => {
    try{    
        const schema = Joi.object({
            chat_id : Joi.string().required()
        })

        const values = await schema.validateAsync(req.query)

        const templates = await adminCtrl.getAdminTemplates(values,req)

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

router.get('/get-template', async(req,res) => {
    try{    
        const schema = Joi.object({
            template_id : Joi.string().required()
        }).unknown(true)

        const values = await schema.validateAsync(req.query)

        const templates = await adminCtrl.getTemplate(values,req)

        res.status(200).send({
            "metadata": {
                message : 'every thing is okay'
            },
            "body": {
                "type": "object",
                "data": templates[0]
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

router.delete('/delete-custom-template', async(req,res) => {
    try{    
        const schema = Joi.object({
            template_id : Joi.number().optional()
        })

        const values = await schema.validateAsync(req.body)

        await adminCtrl.deleteCustomTemplate(values,req)

        res.status(200).send({
            "metadata": {
                message : 'every thing is okay'
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

router.get('/get-custom-templates', async(req,res) => {
    try{    
        const schema = Joi.object({
            chat_id : Joi.string().required()
        })

        const values = await schema.validateAsync(req.query)

        const templates = await adminCtrl.getCustomTemplates(values,req)

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

router.get('/get-custom-templates-for-assign', async(req,res) => {
    try{    
        const schema = Joi.object({
            chat_id : Joi.string().required(),
            user_id : Joi.string().required()
        }).unknown(true)

        const values = await schema.validateAsync(req.query)

        const templates = await adminCtrl.getCustomTemplatesForAssignment(values,req)

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

router.get('/get-user-purchase-from-custom-template', async(req,res) => {
    try{    
        const schema = Joi.object({
            chat_id : Joi.string().required(),
            user_id : Joi.string().required()
        }).unknown(true)

        const values = await schema.validateAsync(req.query)

        const templates = await adminCtrl.getUserPurchaseFromCustomTemplate(values,req)

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

router.get('/get-assigned-custom-template', async(req,res) => {
    try{    
        const schema = Joi.object({
            chat_id : Joi.string().required(),
            user_id : Joi.string().required()
        }).unknown(true)

        const values = await schema.validateAsync(req.query)

        const templates = await adminCtrl.getAssignedCustomTemplate(values,req)

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


router.post('/assign-template', async(req,res) => {
    try{    

        const schema = Joi.object({
            template_id : Joi.number().required(),
            user_chat_id : Joi.number().required()
        })
        console.log('hii');
        const values = await schema.validateAsync(req.body)

        await adminCtrl.assignTemplate(values,req)

        res.status(200).send({
            "metadata": {
                message : 'every thing is okay'
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

router.delete('/delete-assignment', async(req,res) => {
    try{    
        const schema = Joi.object({
            user_chat_id : Joi.string().required(),
            template_id : Joi.number().required()
        })

        const values = await schema.validateAsync(req.body)

        await adminCtrl.deleteAssignment(values,req)
        
        res.status(200).send({
            "metadata": {
                "message" : 'every thing is okay'
            }
        })

    }catch(err){
        let message = 'error happend bad request'
        
        if (err.details){
            message = 'invalid input'
        }

        return res.status(400).send({
            "metadata": {
                "message" : message
            }
        })
    }
}) 

router.patch('/reduce-user-debt', async(req,res) => {
    try{    

        const schema = Joi.object({
            amount : Joi.number().required(),
            user_chat_id : Joi.number().required()
        })

        const values = await schema.validateAsync(req.body)

        await adminCtrl.reduceUserDebt(values,req)

        res.status(200).send({
            "metadata": {
                message : 'every thing is okay'
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

module.exports = router