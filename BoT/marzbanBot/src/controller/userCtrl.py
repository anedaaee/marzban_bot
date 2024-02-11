import requests


class User:

    def __init__(self, url_prefix):
        self.url_prefix = url_prefix

    def getUser(self, chat_id):
        response = requests.get(self.url_prefix + f"/user/check-user?chat_id={chat_id}")
        return response

    def getConfigs(self, chat_id):
        response = requests.get(self.url_prefix + f"/user/get-configs?chat_id={chat_id}")
        return response

    def getTemplate(self, template_id):
        response = requests.get(self.url_prefix + f"/user/get-config?template_id={template_id}")
        return response

    def purchase(self,config_name,chat_id,template_id):
        response = requests.post(
            url=self.url_prefix+"/user/purchase",
            data={
                "chat_id":chat_id,
                "template_id":template_id,
                "name":config_name
            }
        )

        return response

    def getHistory(self,chat_id):
        response = requests.get(
            url=f"{self.url_prefix}/user/get-account-debt-history?chat_id={chat_id}"
        )
        return response

    def getConfigLink(self,id):
        response = requests.post(
            url=f"{self.url_prefix}/user/get-config-link?id={id}"
        )
        return response

