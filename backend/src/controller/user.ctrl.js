const request = require('../db/request')
const axios = require('axios')
require('dotenv').config(__dirname+'/.env')

exports.checkUser = async (values,req) => {
    try{
        let query = 'SELECT * FROM KianDB.users WHERE chat_id = ? ;'

        const user = await request(query,[values.chat_id],req)
        
        if (user.length !== 0){
            if(user[0].relevantAdmin){
                query = 'SELECT username FROM KianDB.users WHERE chat_id = ?' 
                
                const admin = await request(query,[user[0].relevantAdmin],req)
                
                user[0]['relevantAdminUsername'] = admin[0].username
            }else{
                user[0]['relevantAdminUsername'] = null
            }
        }else{
            
        }
        return user
    }catch(err){throw err}
}

exports.newUser = async (values,req) => {
    try{
        let query = `INSERT INTO KianDB.users
            (chat_id, name, username, debt, config_name, admit, spam, rule, relevantAdmin, phone)
            VALUES(?, ?, ?, 0, ?, 0, 0, 'user', '', ?);`

        
        await request(query,[values.chat_id,values.name,values.username,values.config_name?values.config_name:'',values.phone],req)

    }catch(err){throw err}
}

exports.getConfigs = async (values,req) => {
    try{
        let query = `SELECT DISTINCT *
                        FROM KianDB.templates WHERE template_id IN (SELECT template_id  FROM KianDB.user_template WHERE chat_id = ?) AND isActive=1;`

        const templates = await request(query,[values.chat_id],req)

        return templates
    }catch(err){throw err}
}

exports.getTemplate = async (values,req) => {
    try{
        let query = `SELECT DISTINCT *
                        FROM KianDB.templates WHERE template_id = ? ;`

        const templates = await request(query,[values.template_id],req)

        return templates
    }catch(err){throw err}
}

exports.purchase = async (values,req) => {
    try{
        let admin_new_price,query2 = '';

        let query = `SELECT debt FROM KianDB.users WHERE chat_id = ? ;`

        const debt = await request(query,[values.chat_id],req)

        query = `SELECT price,whoCreated,parent_template_id FROM KianDB.templates WHERE template_id = ? ;`

        const price = await request(query,[values.template_id],req)

        const new_price = debt[0].debt + price[0].price

        query = `UPDATE KianDB.users
            SET debt= ?
            WHERE chat_id= ?;`

        await request(query,[new_price , values.chat_id] , req)

        query = `INSERT INTO KianDB.purchase
            (chat_id, created_at, template_id, name)
            VALUES(?, ?, ?, ?);`

        const today = new Date()

        await request(query,[values.chat_id,today,values.template_id,values.name],req)

        if(price[0].whoCreated !== 'manager'){


            query = `SELECT debt FROM KianDB.users WHERE chat_id = ? ;`
            
            const adminDebt = await request(query,[price[0].whoCreated],req)
            
            query = `SELECT price FROM KianDB.templates WHERE template_id = ? ;`

            const adminPrice = await request(query,[price[0].parent_template_id],req)

            admin_new_price = adminDebt[0].debt + adminPrice[0].price

            query = `UPDATE KianDB.users
                SET debt= ?
                WHERE chat_id= ?;`
            
            console.log(query)
            await request(query,[admin_new_price , price[0].whoCreated] , req)

            query2 = `INSERT INTO KianDB.purchase
            (chat_id, created_at, template_id, name)
            VALUES(?, ?, ?, ?);`


            await request(query2,[price[0].whoCreated,today,price[0].parent_template_id,values.name],req)
        }

        query = `SELECT days_limit, data_limit, template_id, price, user_limit, in_bounds, whoCreated, parent_template_id, isActive
        FROM KianDB.templates
        WHERE template_id=?;`

        const tempalte = await request(query,[values.template_id],req)

        const config = await generateConfig(tempalte[0],values)

        return config
    }catch(err){throw err}
}

const generateConfig = async(template,values) => {
    try{
        let expire , date = new Date()
        if (template.days_limit == null){
            expire = null
        }else{
            expire = Math.floor(date.getTime() / 1000) + 86400 * (template.days_limit + 1)
        }
        let data_limit = template.data_limit * 1024 ** 3
        console.log(expire);
        let payload = {
            'username': values.name,
            'proxies': {
                'vless': {}
            },
            'inbounds': JSON.parse(template.in_bounds),
            'on_hold_expire_duration': expire,
            'status' : 'on_hold',
            'data_limit': data_limit,
            'data_limit_reset_strategy': 'no_reset'
        }
        console.log(payload); 
        let headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${process.env.TOKEN}`
        }

        let url = `${process.env.PANEL_URL}/api/user`
        
        const config = await axios.post(url,payload,{headers,retry : false}) 

        return config
    }catch(err){throw err}
}

exports.getAccountDebt_history = async (values,req) => {
    try{

        let query = `SELECT debt FROM KianDB.users WHERE chat_id = ? ;`

        const debt =  await request(query,[values.chat_id],req)

        query = `SELECT DISTINCT purchase.created_at, purchase.id, purchase.name , templates.price , templates.days_limit , templates.data_limit , templates.user_limit , templates.in_bounds
            FROM KianDB.purchase
            JOIN KianDB.templates
            on purchase.template_id = templates.template_id 
            WHERE chat_id = ?`

        const history = await request(query,[values.chat_id],req);

        return {
            debt : debt[0].debt,
            history : history
        }
    }catch(err){throw err}
}

exports.getConfigLink = async (values,req) => {
    try{

        let query = `SELECT name
            FROM KianDB.purchase 
            WHERE id = ?`

        let configName = await request(query,[values.id],req);

        configName = configName[0]

        let config = await getConfig(configName.name)
        return {
            config_name : configName.name,
            config : config
        }
    }catch(err){throw err}
}  

const getConfig = async(configName) => {
    try{

        let headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${process.env.TOKEN}`
        }

        let url = `${process.env.PANEL_URL}/api/user/${configName}`
        
        const config = await axios.get(url,{headers,retry : false}) 

        return {
            "expire": config.data.status == 'on_hold' && ! config.data.expire?  'not started yet' : config.data.expire,
            "data_limit": config.data.data_limit,
            "name":config.data.username,
            "status":config.data.status,
            "subscription_url":config.data.subscription_url
        }
        
    }catch(err){throw err}
}