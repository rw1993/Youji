from weibo import APIClient



class pachong:
    def __init__(self):
	Appkey="367162776"
        Appsecret="059f286cb49d0d922dd22aa83b5853d9"
        callbackurl="http://0.0.0.0:8080/get_code"
        ack="2.00ZkgstF0QoZq5f83044744b0vzHX9"
        expin="1575857235"
        self.client=APIClient(app_key=Appkey,app_secret=Appsecret,redirect_uri=callbackurl)
        self.client.set_access_token(ack,expin)

    def getClient(self):
        return self.client
