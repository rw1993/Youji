import web
import pymongo
render=web.template.render("template")
con=pymongo.Connection("localhost",27017)
Youji=con.Youji
activities=Youji.activities
urls=(
   "/activity","show_activity",
   "/index","index",
   "/search","activity_list",
        )

app=web.application(urls,globals())

class activity_list:
    def POST(self):
        webinput=web.input()
        id_list=[]
        name=webinput[u'name']
        for activity in activities.find():
            if str(name)==str(activity[u'begin_status'][u'user'][u'screen_name']):
                if activity[u'state']=="finish":
                    id_list.append(activity[u'begin_id'])
        return render.activity_list(id_list)

class index:
    def GET(self):
        return render.index()

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
