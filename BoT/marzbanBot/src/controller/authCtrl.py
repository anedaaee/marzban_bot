import requests

class Authorization:

    def __init__(self,url_prefix):
        self.url_prefix = url_prefix

    def checkUser(self,chat_id):
        response = requests.get(self.url_prefix+f"/user/check-user?chat_id={chat_id}")
        return response

    def newUser(self,chat_id,name,username,phone,config_name):
        response = requests.post(
            self.url_prefix+f"/user/new-user",
            {
                "chat_id":chat_id,
                "name":name,
                "username":username,
                "phone":phone,
                "config_name":config_name
            }
        )
        return response