from GetWeiBo import pachong
import pymongo
con=pymongo.Connection("localhost",27017)
Youji=con.Youji
activities=Youji.activities
p=pachong()
client=p.getClient()
begin_str=u"\u65c5\u7a0b\u5f00\u59cb"
end_str=u"\u65c5\u7a0b\u7ed3\u675f"
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
                result[u'end_status']=status
                result[u'state']="finish"
                updata(result)
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


