import requests


class Admin:

    def __init__(self, url_prefix):
        self.url_prefix = url_prefix

    def reduceUserDebt(self,chat_id,user_id,amount):
        response = requests.patch(f"{self.url_prefix}/admin/reduce-user-debt?chat_id={chat_id}",
                                data = {
                                    "amount":amount,
                                    "user_chat_id":user_id
                                })
        return response


    def getUsers(self,chat_id):
        response = requests.get(f"{self.url_prefix}/admin/get_users?chat_id={chat_id}")
        return response

    def getAdminTemplates(self,chat_id):
        response = requests.get(f"{self.url_prefix}/admin/get-admin-templates?chat_id={chat_id}")
        return response

    def addTemplate(self,chat_id,template_id,new_price):
        response = requests.post(f"{self.url_prefix}/admin/add-template?chat_id={chat_id}",data={
            "template_id":template_id,
            "new_price":new_price
        })
        return response

    def getTemplate(self,chat_id,template_id):
        response = requests.get(f"{self.url_prefix}/admin/get-template?chat_id={chat_id}&template_id={template_id}")
        return response

    def getCustomTemplate(self,chat_id):
        response = requests.get(f"{self.url_prefix}/admin/get-custom-templates?chat_id={chat_id}")
        return response

    def getCustomTemplateForAssign(self,chat_id,user_id):
        response = requests.get(f"{self.url_prefix}/admin/get-custom-templates-for-assign?chat_id={chat_id}&user_id={user_id}")
        return response
    def deleteTempalte(self,chat_id,template_id):
        response = requests.delete(f"{self.url_prefix}/admin/delete-custom-template?chat_id={chat_id}",data={
            "template_id":template_id
        })
        return response

    def assignTemplate(self,chat_id,user_id,template_id):
        response = requests.post(f"{self.url_prefix}/admin/assign-template?chat_id={chat_id}",data={
            "user_chat_id":user_id,
            "template_id":template_id
        })
        return response

    def assignTemplate(self,chat_id,user_id,template_id):
        response = requests.post(f"{self.url_prefix}/admin/assign-template?chat_id={chat_id}",data={
            "user_chat_id":user_id,
            "template_id":template_id
        })
        return response

    def getPurchaseFromCustomTemplate(self,chat_id,user_id):
        response = requests.get(f"{self.url_prefix}/admin/get-user-purchase-from-custom-template?chat_id={chat_id}&user_id={user_id}")
        return response

    def getAssignedTemplate(self,chat_id,user_id):
        response = requests.get(f"{self.url_prefix}/admin/get-assigned-custom-template?chat_id={chat_id}&user_id={user_id}")
        return response

    def deleteAssignment(self,chat_id,user_id,template_id):
        response =requests.delete(f"{self.url_prefix}/admin/delete-assignment?chat_id={chat_id}",data={
            "user_chat_id":user_id,
            "template_id":template_id
        })
        return response