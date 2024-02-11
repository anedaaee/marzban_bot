import requests


class Manager:

    def __init__(self, url_prefix):
        self.url_prefix = url_prefix

    def getUsers(self, chat_id):
        response = requests.get(self.url_prefix + f"/manager/get-users?chat_id={chat_id}")
        return response

    def getAdmins(self, chat_id):
        response = requests.get(self.url_prefix + f"/manager/get-admins?chat_id={chat_id}")
        return response

    def assignAdmin(self, chat_id,user_id,admin_id):
        response = requests.patch(self.url_prefix + f"/manager/assign-admin?chat_id={chat_id}"
                                ,data={
                                    "relevantAdmin":admin_id,
                                    "user_chat_id":user_id
                                }
            )
        return response

    def bannUser(self,chat_id,user_id):
        response = requests.patch(self.url_prefix + f"/manager/bann-user?chat_id={chat_id}"
                                  , data={
                                        "user_chat_id": user_id
                                }
                            )

        return response

    def getTemplates(self,chat_id):
        response = requests.get(f"{self.url_prefix}/manager/get-templates?chat_id={chat_id}")
        return response
    def getTemplate(self,chat_id,template_id):
        response = requests.get(f"{self.url_prefix}/manager/get-template?chat_id={chat_id}&template_id={template_id}")
        return response

    def deleteTemplate(self,chat_id,template_id):
        response = requests.delete(f"{self.url_prefix}/manager/delete-template?chat_id={chat_id}",data={"template_id":template_id})
        return response
    def assignTemplate(self,chat_id,user_id,template_id):
        response = requests.post(f"{self.url_prefix}/manager/assign-template?chat_id={chat_id}", data={
            "user_chat_id":user_id,
            "template_id":template_id
        })

        return response
    def deleteAssignedTemplate(self,chat_id,user_id,template_id):
        response = requests.delete(f"{self.url_prefix}/manager/delete-assignment?chat_id={chat_id}", data={
            "user_chat_id":user_id,
            "template_id":template_id
        })

        return response

    def alterUser(self,chat_id,user_id,rule):
        response = requests.patch(f"{self.url_prefix}/manager/alter-user?chat_id={chat_id}",
                                 data={
                                    "user_chat_id":user_id,
                                     "rule":rule
                                 })
        return response

    def getNoneAdmitUsers(self,chat_id):
        response = requests.get(f"{self.url_prefix}/manager/get-none-admit-users?chat_id={chat_id}")

        return response

    def admitNewUser(self,chat_id,user_id):
        response = requests.patch(f"{self.url_prefix}/manager/admit-user?chat_id={chat_id}",data={"user_chat_id":user_id})
        return response

    def getSpamUsers(self,chat_id):
        response = requests.get(f"{self.url_prefix}/manager/get-banned-users?chat_id={chat_id}")

        return response

    def unbannUser(self,chat_id,user_id):
        response = requests.patch(f"{self.url_prefix}/manager/unbann-user?chat_id={chat_id}",data={"user_chat_id":user_id})
        return response

    def addTemplate(self,chat_id,days_limit,data_limit,price,user_limit,in_bounds):
        response = requests.post(f"{self.url_prefix}/manager/add-template?chat_id={chat_id}",data={
            "days_limit":days_limit,
            "data_limit":data_limit,
            "price":price,
            "user_limit":user_limit,
            "in_bound":in_bounds
        })
        return response