from GetWeiBo import pachong
import pymongo
import pdfcrowd
con=pymongo.Connection("localhost",27017)
Youji=con.Youji
activities=Youji.activities
p=pachong()
client=p.getClient()
begin_str=u"\u65c5\u7a0b\u5f00\u59cb"
end_str=u"\u65c5\u7a0b\u7ed3\u675f"
def savepdf(result):
    filename=str(result[u'begin_id'])
    filename+=".pdf"
    client=pdfcrowd.Client("rw1993","d46f29fedccb37abefde8cfdf5d9206c")
    fileurl="../static/"+filename
    f=file(fileurl,"w")
    uri="http://0.0.0.0:8080/activity?id="+str(result[u'begin_id'])
    client.convertURI(uri,f)
def send_weibo(status,begin_id):
    string=u'\u60a8\u7684\u6e38\u8bb0\u5df2\u7ecf\u751f\u6210'+' link='
    ids=str(begin_id)
    url="http://0.0.0.0:8080/activity?id="+ids
    string+=url
    name=status[u'user'][u'screen_name']
    pdflink="http://0.0.0.0:8080/activity?id="+ids
    string+=" pdf="+pdflink
    string+=u' @'
    string+=name
    client.statuses.update.post(status=string)
def download(page,since_id):
    data=client.statuses.mentions.get(count=200,page=page,since_id=since_id)
    return data[u'statuses']
def get_since_id():
    result=activities.find_one({u'ifsince_id':True})
    if result is None:
        return 0
    else:
        return result[u'since_id']

def begin_activity(status):
    print status[u'id']
    activity={}
    his_infor=status[u'user']
    activity[u'host_uid']=his_infor['id']
    activity[u'begin_id']=status[u'id']
    activity[u'begin_status']=status
    activity[u'state']="begin"
    activity[u'statuses']=[]
    activity[u'statuses'].append(status)
    activities.insert(activity)
def updata(result):
    activities.remove({u'begin_id':result[u'begin_id']})
    activities.insert(result)

def analyze(status):
    his_infor=status[u'user']
    his_uid=his_infor[u'id']
    #if a current activity host by him
    results=activities.find({u'host_uid':his_uid})
    ifbegin=True
    for result in results:
        print result['begin_id']
        print status['id']
        if result[u'state']=="begin" and result[u'begin_id']<status[u'id']:
            ifbegin=False
            if end_str in status[u'text']:
                result[u'statuses'].append(status)
                result[u'state']="finish"
                updata(result)
                #savepdf(result)
                send_weibo(status,result[u'begin_id'])
            else:
                result[u'statuses'].append(status)
                updata(result)

    if begin_str in status[u'text']:
        if ifbegin:
            begin_activity(status)

    



if __name__=="__main__":
    lenth=200
    page=1
    since_id=get_since_id()
    statuses=[]
    print "downloading"
    while lenth>190:
        statuses+=download(page,since_id)
        page+=1
        lenth=len(statuses)
    for status in statuses[::-1]:
        if status[u'id']>since_id:
            since_id=status[u'id']
            analyze(status)

    if get_since_id==0:
        since_id_={}
        since_id_[u'if_since_id']=True
        since_id_[u'since_id']=since_id
        activities.insert(since_id_)
    else:
        activities.update({u'if_since_id':True},{"$set":{u'since_id':since_id}})


