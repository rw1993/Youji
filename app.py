import web
import pymongo
render=web.template.render("template")
con=pymongo.Connection("localhost",27017)
Youji=con.Youji
activities=Youji.activities
urls=(
   "/activity","show_activity"
        )

app=web.application(urls,globals())

class show_activity:
    def GET(self):
        webinput=web.input()
        begin_id=webinput[u'id']
        activity=activities.find_one({u'begin_id':int(begin_id)})
        if activity is None:
            return "No such activity"
        else:
            if activity[u'state']=="finish":
                return render.activity(activity)
            else:
                return "activity not finish"

if __name__=="__main__":
    app.run()
