const request = require('../db/request')

exports.getUsers = async(values,req) => {
    try{
        let query = `SELECT * FROM KianDB.users WHERE relevantAdmin=? ;`

        const users = await request(query,[values.chat_id],req)

        return users

    }catch(err){throw err}
}

exports.addTemplate = async(chat_id,values,req) => {
    try{
        let query = `SELECT * FROM KianDB.templates WHERE template_id=? ;`

        const template = await request(query,[values.template_id],req)

        query = `INSERT INTO KianDB.templates
                (days_limit, data_limit, price, user_limit, in_bounds, whoCreated , parent_template_id)
                VALUES(?, ?, ?, ?, ?, ? ,?);`


        await request(query,[template[0].days_limit,template[0].data_limit,values.new_price,template[0].user_limit,template[0].in_bounds,chat_id.chat_id,values.template_id],req)
        

    }catch(err){throw err}
}

exports.getAdminTemplates = async(values,req) => {
    try{
        let query = `SELECT * FROM KianDB.templates WHERE template_id IN (SELECT template_id  FROM KianDB.user_template WHERE chat_id = ?) AND isActive=1;`

        const templates = await request(query,[values.chat_id],req)

        return templates;

    }catch(err){throw err}
}

exports.getCustomTemplates = async(values,req) => {
    try{
        let query = `SELECT * FROM KianDB.templates WHERE whoCreated=? AND isActive=1;`

        const templates = await request(query,[values.chat_id],req)

        return templates;

    }catch(err){throw err}
}
exports.getCustomTemplatesForAssignment = async(values,req) => {
    try{
        let query = `SELECT * FROM KianDB.templates WHERE whoCreated=? AND isActive=1 and template_id NOT IN (SELECT template_id FROM KianDB.user_template WHERE chat_id = ?);`

        const templates = await request(query,[values.chat_id,values.user_id],req)

        return templates;

    }catch(err){throw err}
}
exports.getUserPurchaseFromCustomTemplate = async(values,req) => {
    try{
        let query = `SELECT p.chat_id ,p.created_at ,p.template_id ,p.name , t.price ,t.days_limit ,t.data_limit ,t.user_limit ,t.in_bounds  
        FROM KianDB.purchase p 
        INNER JOIN KianDB.templates t 
        ON p.template_id = t.template_id 
        WHERE p.template_id NOT IN (SELECT template_id FROM KianDB.templates t WHERE t.whoCreated = 'manager')
        AND t.whoCreated = ?
        AND p.chat_id = ?;`

        const templates = await request(query,[values.chat_id,values.user_id],req)

        return templates;

    }catch(err){throw err}
}
exports.getAssignedCustomTemplate = async(values,req) => {
    try{
        let query = `SELECT ut.chat_id , ut.template_id , t.days_limit ,t.data_limit ,t.user_limit ,t.in_bounds ,t.price  FROM 
        KianDB.user_template ut
        INNER JOIN
        KianDB.templates t
		ON ut.template_id = t.template_id
        WHERE 
        ut.template_id IN (
            SELECT template_id 
            FROM KianDB.templates t2 
            WHERE t2.whoCreated = ?
        )
        AND chat_id = ?;`

        const templates = await request(query,[values.chat_id,values.user_id],req)

        return templates;

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
exports.deleteCustomTemplate = async(values,req) => {
    try{
        let query = `UPDATE KianDB.templates
        SET isActive=0
        WHERE template_id=?;`

        await request(query,[values.template_id],req)

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

exports.reduceUserDebt = async(values,req) => {
    try{

        let query = `SELECT debt
            FROM KianDB.users
            WHERE chat_id = ?;`

        const debt = await request(query,[values.user_chat_id],req)

        if(debt.length !== 0){
            newDebt = debt[0].debt - values.amount

            query = `UPDATE KianDB.users
                SET debt=?
                WHERE chat_id=?;`
            
            await request(query,[newDebt , values.user_chat_id],req)
        }


    }catch(err){throw err}
}

