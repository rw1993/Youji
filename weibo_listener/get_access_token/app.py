import web
from weibo import APIClient

urls=(
        "/get_code","get_code",
        )
app=web.application(urls,globals())
class get_code:
    def GET(self):
        webinput=web.input()
        code=webinput[u'code']
        client=APIClient(app_key="367162776",app_secret="059f286cb49d0d922dd22aa83b5853d9",redirect_uri="http://0.0.0.0:8080/get_code")
        r=client.request_access_token(code)
        print r[u'access_token']
        print r[u'expires_in']
        return "hello"
if __name__=='__main__':
    app.run()
