from weibo import APIClient



class pachong:
    def __init__(self):
	Appkey="367162776"
        Appsecret="059f286cb49d0d922dd22aa83b5853d9"
        callbackurl="http://www.baidu.com"
        ack="2.00ZkgstF3mz1gEe89b68d8f9TXrgUE"
        expin="7837801"
        self.client=APIClient(app_key=Appkey,app_secret=Appsecret)
        self.client.set_access_token(ack,expin)

    def getClient(self):
        return self.client
