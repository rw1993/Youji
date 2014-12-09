import pdfcrowd

try:
    client=pdfcrowd.Client("rw1993","d46f29fedccb37abefde8cfdf5d9206c")
    f=file("baidu.pdf","w")
    pdf=client.convertURI("http://www.baidu.com",f)
    f.close()
except:
    print "error"
