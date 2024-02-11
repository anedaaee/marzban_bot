const express = require('express')
const Joi = require('joi')
const managerCtrl = require('../controller/manager.ctrl')
const router = new express.Router()

router.get('/get-users', async(req,res) => {
    try{    

        const users = await managerCtrl.getUsers(req)

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

router.get('/get-none-admit-users', async(req,res) => {
    try{    

        const users = await managerCtrl.getNoneAdmitUsers(req)

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

router.get('/get-banned-users', async(req,res) => {
    try{    

        const users = await managerCtrl.getBannedUser(req)

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

router.get('/get-admins', async(req,res) => {
    try{    

        const users = await managerCtrl.getAdmin(req)

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

router.patch('/alter-user', async(req,res) => {
    try{    
        const schema = Joi.object({
            user_chat_id : Joi.string().required(),
            rule : Joi.string().required()
        })

        const values = await schema.validateAsync(req.body)

        await managerCtrl.alterUser(values,req)

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

router.patch('/admit-user', async(req,res) => {
    try{    
        const schema = Joi.object({
            user_chat_id : Joi.string().required(),
        })

        const values = await schema.validateAsync(req.body)

        await managerCtrl.admitUser(values,req)

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


router.patch('/bann-user', async(req,res) => {
    try{    
        const schema = Joi.object({
            user_chat_id : Joi.string().required(),
        })

        const values = await schema.validateAsync(req.body)

        await managerCtrl.bannUser(values,req)

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


router.patch('/unbann-user', async(req,res) => {
    try{    
        const schema = Joi.object({
            user_chat_id : Joi.string().required(),
        })

        const values = await schema.validateAsync(req.body)

        await managerCtrl.unBannUser(values,req)

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

router.patch('/assign-admin', async(req,res) => {
    try{    
        const schema = Joi.object({
            relevantAdmin : Joi.string().required(),
            user_chat_id : Joi.string().required(),
        })

        const values = await schema.validateAsync(req.body)

        await managerCtrl.assignAdmin(values,req)

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

router.post('/add-template', async(req,res) => {
    try{    
        const schema = Joi.object({
            days_limit : Joi.number().optional(),
            data_limit : Joi.number().optional(),
            price : Joi.number().required(),
            user_limit : Joi.string().optional(),
            in_bound: Joi.string().optional(),
        })

        const values = await schema.validateAsync(req.body)

        await managerCtrl.addTemplate(values,req)

        res.status(200).send({
            "metadata": {
                message : 'every thing is okay'
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

router.delete('/delete-template', async(req,res) => {
    try{    
        const schema = Joi.object({
            template_id : Joi.number().optional()
        })

        const values = await schema.validateAsync(req.body)

        await managerCtrl.deleteTemplate(values,req)

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


router.get('/get-templates', async(req,res) => {
    try{    

        const templates = await managerCtrl.getTemplates(req)
        
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
        console.log('hi');
        const schema = Joi.object({
            template_id : Joi.number().required()
        }).unknown(true)

        const values = await schema.validateAsync(req.query)

        const template = await managerCtrl.getTemplate(values,req)

        res.status(200).send({
            "metadata": {
                "message" : 'every thing is okay'
            },
            "body": {
                "type": "array",
                "data": template[0]
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


router.post('/assign-template', async(req,res) => {
    try{    
        const schema = Joi.object({
            user_chat_id : Joi.string().required(),
            template_id : Joi.number().required()
        })

        const values = await schema.validateAsync(req.body)

        await managerCtrl.assignTemplate(values,req)

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

router.delete('/delete-assignment', async(req,res) => {
    try{    
        const schema = Joi.object({
            user_chat_id : Joi.string().required(),
            template_id : Joi.number().required()
        })

        const values = await schema.validateAsync(req.body)

        await managerCtrl.deleteAssignment(values,req)
        
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

module.exports = router