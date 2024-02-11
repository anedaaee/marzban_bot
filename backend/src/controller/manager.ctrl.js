const request = require('../db/request')



exports.getUsers = async(req) => {
    try{
        let query = `SELECT * FROM KianDB.users WHERE admit =1 and spam=0 and (rule='user' or rule='admin');`

        const users = await request(query,[],req)

        return users

    }catch(err){throw err}
}

exports.getNoneAdmitUsers = async(req) => {
    try{
        let query = `SELECT * FROM KianDB.users WHERE admit =0 ;`

        const users = await request(query,[],req)

        return users

    }catch(err){throw err}
}

exports.getBannedUser = async(req) => {
    try{
        let query = `SELECT * FROM KianDB.users WHERE spam =1 ;`

        const users = await request(query,[],req)

        return users

    }catch(err){throw err}
}

exports.getAdmin = async(req) => {
    try{
        let query = `SELECT * FROM KianDB.users WHERE rule = 'admin';`

        const users = await request(query,[],req)

        return users

    }catch(err){throw err}
}

exports.alterUser = async(values,req) => {
    try{
        let query = `UPDATE KianDB.users
        SET rule= ?
        WHERE chat_id= ? ;`

        await request(query,[values.rule,values.user_chat_id],req)

    }catch(err){throw err}
}

exports.admitUser = async(values,req) => {
    try{
        let query = `UPDATE KianDB.users
            SET admit= 1
            WHERE chat_id= ? ;`

        await request(query,[values.user_chat_id],req)

    }catch(err){throw err}
}



exports.bannUser = async(values,req) => {
    try{
        let query = `UPDATE KianDB.users
            SET spam= 1
            WHERE chat_id= ? ;`

        await request(query,[values.user_chat_id],req)

    }catch(err){throw err}
}

exports.unBannUser = async(values,req) => {
    try{
        let query = `UPDATE KianDB.users
            SET spam= 0
            WHERE chat_id= ? ;`

        await request(query,[values.user_chat_id],req)

    }catch(err){throw err}
}

exports.assignAdmin = async(values,req) => {
    try{
        let query = `UPDATE KianDB.users
            SET relevantAdmin= ?
            WHERE chat_id= ? ;`

        await request(query,[values.relevantAdmin,values.user_chat_id],req)

    }catch(err){throw err}
}

exports.addTemplate = async(values,req) => {
    try{
        let query = `INSERT INTO KianDB.templates
        (days_limit, data_limit, price, user_limit, in_bounds, whoCreated)
        VALUES(?, ?, ?, ?, ?, 'manager');`

        await request(query,[values.days_limit?values.days_limit:null,values.data_limit?values.data_limit:null,values.price,values.user_limit?values.user_limit:null,values.in_bound?values.in_bound:null ],req)

    }catch(err){throw err}
}

exports.deleteTemplate = async(values,req) => {
    try{
        let query = `UPDATE KianDB.templates
        SET isActive=0
        WHERE template_id=?;`

        await request(query,[values.template_id],req)

    }catch(err){throw err}
}

exports.getTemplates = async(req) => {
    try{
        let query = `SELECT DISTINCT days_limit, data_limit, template_id, price, user_limit, in_bounds, whoCreated, parent_template_id
        FROM KianDB.templates
        WHERE isActive = 1 ;`
            

        const templates = await request(query,[],req)
        
        return templates

    }catch(err){throw err}
}

exports.getTemplate = async(values,req) => {
    try{
        let query = `SELECT DISTINCT days_limit, data_limit, template_id, price, user_limit, in_bounds, whoCreated, parent_template_id
        FROM KianDB.templates
        WHERE template_id = ? and isActive=1;`
            
        const template = await request(query,[values.template_id],req)

        return template

    }catch(err){throw err}
}

exports.assignTemplate = async(values,req) => {
    try{
        let query = `INSERT INTO KianDB.user_template
            (chat_id, template_id)
            VALUES(?, ?);`
            

        await request(query,[values.user_chat_id,values.template_id],req)

    }catch(err){throw err}
}

exports.deleteAssignment = async(values,req) => {
    try{
        let query = `DELETE FROM KianDB.user_template
            WHERE chat_id=? AND template_id=?;`
            

        await request(query,[values.user_chat_id,values.template_id],req)

    }catch(err){throw err}
}