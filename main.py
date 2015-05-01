import urllib2
import urllib
import sys
#isolate ID
def fmtId(string):
    return string[1:len(string) - 1]


#Talk to people
def talk(id,req):

    #Show the server that we're typing
    typing = urllib2.urlopen('http://omegle.com/typing', '&id='+id)
    typing.close()

    #Show the user that we can write now
    msg = str(raw_input('> '))

    #Send the string to the stranger ID
    msgReq = urllib2.urlopen('http://omegle.com/send', '&msg='+msg+'&id='+id)

    #Close the connection
    msgReq.close()


#This is where all the magic happens, we listen constantly to the page for events
def listenServer(id, req):
    while True:
        site = urllib2.urlopen(req)

        #We read the HTTP output to get what's going on
        rec = site.read()

        if 'waiting' in rec:
            print("Waiting...")

        elif 'error' in rec:
            # print(rec)
            if 'You are temporarily banned' in rec:
                print('You are temporarily banned')
                #close connection or retry with new url(mirrors); could also use new IP, but impractical.
                sys.exit('');
                if 'antinudeservers' in rec:
                    print('You are temporarily banned: Suspected by antinudeservers')
                    sys.exit('');
            #other possible errors

        elif 'connected' in rec:
            print('Connected')
            print(id)
            talk(id,req)
            
        elif 'strangerDisconnected' in rec:
            print('Stranger Disconnected')
            #restart
            omegleConnect()
            
        elif 'typing' in rec:
            print("Stranger is typing...")

        #print message and talk          
        elif 'gotMessage' in rec:
            print(rec[16:len(rec) - 2])
            talk(id,req)

def omegleConnect():
    opener = urllib2.build_opener()

    ##add in the topiclist data
    # topiclist = '["14","15","16"]'
    # opener.addheaders.append(('Cookie', 'topiclist='+topiclist))
    # site = opener.open('http://omegle.com/start')
    site = urllib2.urlopen('http://omegle.com/start','')
    id = fmtId(site.read())
    
    print(id)
    req = urllib2.Request('http://omegle.com/events', urllib.urlencode({'id':id}))
    print('Searching for users')
    listenServer(id,req)
  
omegleConnect()