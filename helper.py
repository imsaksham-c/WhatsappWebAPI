import requests

HEADERS = {
       'Authorization': 'Bearer EAAqtPYZCt4N0BACOugY6JBkaK7WfVSGWkQL3xQgg2FpWZAjPao0WbTj4uhp11rNjpyUZAPqCZCl8E0MGYvhZBYvvHsvMdZCKntSWQk7QD3DClpRGKP65Jpq1fEeuBiSFnkFZBv6AgiQWournYqYr2e5Ug8RYsmFm8XSEPqsiKGJgMTKAza96qDWasOum4yZAEcdoXZCTYQN6gQQZDZD',}

def send_msg(msg, mob):
    json_data = {
       'messaging_product': 'whatsapp',
       'to': mob,
       'type': 'text',
       "text": {
           "body": msg
       }
    }
    response = requests.post('https://graph.facebook.com/v15.0/112149938479033/messages', headers=HEADERS, json=json_data)
    #print('MESSAGE_SENT-->',response.text)
       
def getAudio(id_):
    status = False
    audioLoc = ''
    url = "https://graph.facebook.com/v13.0/"+id_
    payload={}
    response = (requests.request("GET", url, headers=HEADERS, data=payload)).json()
    nextURL = response['url']
    
    responseNew = requests.request("GET", nextURL, headers=HEADERS, data=payload)
    if responseNew:
        try:
            audioLoc = "./testAudio.mp3"
            with open(audioLoc, 'wb') as f:
                f.write(responseNew.content)
            status = True 
        except:
            status = False
    return status, audioLoc

def getText():
    url = "http://65.2.172.72:4000/getText"

    payload={'session': 'WhatsApp',
    'paid_user': 'True'}
    files=[
      ('file',('testAudio.mp3',open('./testAudio.mp3','rb'),'audio/mpeg'))
    ]
    headers = {}
    response = (requests.request("POST", url, headers=HEADERS, data=payload, files=files)).json()    
    return response['status'], response['response']['data']['Text']
        
        
def processRequest(req):
    mobile = ''
    requestType = ''
    f_status = False
    msg = ''
    
    try:
        mobile = req['entry'][0]['changes'][0]['value']['messages'][0]['from']
        requestType = 'MsgReceived'
    except:
        mobile = req['entry'][0]['changes'][0]['value']['statuses'][0]['recipient_id']
        requestType = 'MsgSent'
        
    print('requestType---------', requestType)
        
    if requestType == 'MsgReceived':
        fileType = req['entry'][0]['changes'][0]['value']['messages'][0]['type']
        
        if fileType == 'audio':
            send_msg('🤖s Working On It.', mobile)
            id_ = req['entry'][0]['changes'][0]['value']['messages'][0]['audio']['id']
            status, audio = getAudio(id_)
            
            if status:
                verify, msg = getText()
                if not verify:
                    msg = '🤖 Error! Bot Couldnot Process Audio.'
            else:
                msg = '🤖 Couldnot Process Audio.'            
        else:
            msg = '🤖 only Processes Audio File! Please Send Audio File.'
        
        send_msg(msg, mobile)
        print('MESSAGE_SENT---->', mobile, msg)
        return True
    
    else:
        return False
            
