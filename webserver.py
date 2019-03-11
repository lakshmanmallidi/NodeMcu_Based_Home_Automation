from socket import socket
from threading import Thread
from time import sleep
from urllib.parse import urlparse
from random import choice
from pyttsx3 import init
from requests import post
def sendsms(msg, to):
    data = {
      'Body': msg,
      'From': '+14254485583',
      'To': '+91'+to
    }
    response = post('https://AC174f4a3c13f6cdd7d5e9898d151c33e9:df47d33c37664ef2fa267195786167af@api.twilio.com/2010-04-01/Accounts/AC174f4a3c13f6cdd7d5e9898d151c33e9/Messages.json',data=data)
    print(response.content)

def nodemcu_getdata_thread():
    global gas, pir
    pirflag = False
    while True:
        s=socket()
        s.connect((nodemcu_ip,nodemcu_port))
        s.send(b"give_data")
        data = s.recv(30)
        s.close()
        a,b = map(int,data.decode().split(","))
        if(a==0 and switch3 and (not pirflag)):
            sendsms("Intrusion alert","7780315201")
            pir = "1"
            pirflag = True
        else:
            if(a==1):
                pir = "0"
            else:
                pir = "1"
            pirflag = False
        if(b>250 and switch4):
            sendsms("Fire alert","7780315201")
            gas = str(b)
        else:
            gas = str(b)
        sleep(10)
        
def speak(data):
    try:
        engine=init()
        engine.setProperty('rate',85)
        engine.say(data)
        engine.runAndWait()
    except Exception as e:
        print(e)
    
def processparameters(client,variables,reqfile):
    global sessionids
    if(variables[0][0]=="username" and variables[1][0]=="password"):
        if(variables[0][1]==username and variables[1][1]==password):
            if(len(variables)==3):
                if variables[2][1] in sessionids:
                    sessionids.remove(variables[2][1])
            client.send(b'Content-Type:text/html\n\n')
            randomsessionid=''.join(choice('0123456789ABCDEF') for i in range(16))
            sessionids.append(randomsessionid)
            client.send(("myhome.html "+randomsessionid).encode())
        else:
            client.send(b'Content-Type:text/html\n\n')
            client.send("loginerror")
    elif(variables[0][0]=="sessionid"):
        if variables[0][1] in sessionids:
            if(reqfile=="getvalue"):
                client.send(b'Content-Type:text/html\n\n')
                client.send((pir+","+gas).encode())
            else:
                client.send(b'Content-Type:text/html\n\n')
                page=open(reqfile,'rb')
                client.send(page.read())
                page.close()
        else:
            client.send(b'Content-Type:text/html\n\n')
            page=open("index.html",'rb')
            client.send(page.read())
            page.close()
    elif(variables[0][0]=="buttonstatus"):
        client.send(b'Content-Type:text/html\n\n')
        client.send((str(switch1)+" "+str(switch2)+" "+str(switch3)+" "+str(switch4)).encode())
    elif(variables[0][0]=="switch1"):
        client.send(b'Content-Type:text/html\n\n')
        client.send(("switch1 "+str(not switch1)).encode())
        toggleswitch1()   
    elif(variables[0][0]=="switch2"):
        client.send(b'Content-Type:text/html\n\n')
        client.send(("switch2 "+str(not switch2)).encode())
        toggleswitch2()
    elif(variables[0][0]=="switch3"):
        client.send(b'Content-Type:text/html\n\n')
        client.send(("switch3 "+str(not switch3)).encode())
        toggleswitch3()
    elif(variables[0][0]=="switch4"):
        client.send(b'Content-Type:text/html\n\n')
        client.send(("switch4 "+str(not switch4)).encode())
        toggleswitch4()
        
def toggleswitch1():
    global switch1
    try:
        switch1 = not switch1
        s = socket()
        s.connect((nodemcu_ip,nodemcu_port))
        if(switch1):
            Thread(target=speak,args=("lights on",)).start()
            s.send(b'switch1_on')
        else:
            Thread(target=speak,args=("lights off",)).start()
            s.send(b'switch1_off')
        s.close()
    except Exception as e:
        print(e)
        
def toggleswitch2():
    global switch2
    try:
        switch2 = not switch2
        s = socket()
        s.connect((nodemcu_ip,nodemcu_port))
        if(switch2):
            Thread(target=speak,args=("Fan on",)).start()
            s.send(b'switch2_on')
        else:
            Thread(target=speak,args=("Fan off",)).start()
            s.send(b'switch2_off')
        s.close()
    except Exception as e:
        print(e)
def toggleswitch3():
    global switch3
    switch3 = not switch3
    if(switch3):
        Thread(target=speak,args=("sms alert for intrusion detection is turned on",)).start()
    else:
        Thread(target=speak,args=("sms alert for intrusion detection is turned off",)).start()
def toggleswitch4():
    global switch4
    switch4 = not switch4
    if(switch4):
        Thread(target=speak,args=("sms alert for gas sensor is turned on",)).start()
    else:
        Thread(target=speak,args=("sms alert for gas sensor is turned off",)).start()
def mainthread(client,addr):
    try:
        print('Got connection from', addr[0],addr[1],"\n")  #printing 1
        fullreq=str(client.recv(1024))
        print(fullreq) #printing 2
        parsedreq=urlparse(fullreq.split(" ")[1])
        client.send(b'HTTP/1.1 200 OK\n')
        reqfile=parsedreq[2][1:]
        filetype=reqfile.split("/")[-1].split(".")[-1]
        print(reqfile) #printing 3
        if(parsedreq[4]!=""):
            query=parsedreq[4]
            querylist=query.split("&")
            variables=[]
            for e in querylist:
                key,data=e.split("=")
                variables.append((" ".join(key.split("+"))," ".join(data.split("+"))))
            print(variables)
            processparameters(client,variables,reqfile)
        else:
            if reqfile=="":
                client.send(b'Content-Type:text/html\n\n')
                page=open("index.html",'rb')
                client.send(page.read())
            elif reqfile=="myhome.html" or reqfile=="livedata.html":
                client.send(b'Content-Type:text/html\n\n')
                page=open("index.html",'rb')
                client.send(page.read()) 
            else:
                if filetype in ctype:
                    client.send(b'Content-Type:'+ctype[filetype].encode()+b'\n\n')
                else:
                    client.send(b'Content-Type:text/html\n\n')
                page=open(reqfile,'rb')
                client.send(page.read())
            page.close()
    except Exception as e:
            print(e)
    client.close()    
if __name__=="__main__":
    switch1=False
    switch2=False
    switch3=False
    switch4=False
    pir = "0"
    gas = "0"
    username="myhome"
    password="sweethome"
    sessionids=[]
    
    s=socket()
    ip=input('Enter server ip address:')
    nodemcu_ip=input('Enter NodeMcu ip address:')
    port=9000
    nodemcu_port=7000
    s.bind((ip,port))
    s.listen(1)
    print("server is running at",ip,":",port)
    ctype={"html":"text/html",
           "htm":"text/html",
           "xml":"text/xml",
           "txt":"text/plain",
           "css":"text/css",
           "png":"image/png",
           "gif":"image/gif",
           "jpg":"image/jpg",
           "jpeg":"image/jpeg",
           "js":"application/javascript",
           "svg":"image/svg+xml",
           "ttf":"application/x-font-ttf",
           "otf":"application/x-font-opentype",
           "woff":"application/font-woff",
           "woff2":"application/font-woff2",
           "eot":"application/vnd.ms-fontobject",
           "sfnt":"application/font-sfnt"}
    Thread(target=nodemcu_getdata_thread).start()
    while True:
        client,address= s.accept()
        Thread(target=mainthread,args=(client,address)).start()
        sleep(0.01)



