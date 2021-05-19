try:
    import os
    import requests
    from flask import Flask, request
except ImportError:
    print('Please install required modules: pip install -r requirements.txt')
    exit()

app = Flask(__name__)
apiurl = 'http://apache'

def apiLogin():
    payload = {'login':'','user':f'{os.environ["USERBD"]}', 'password':f'{os.environ["PASSWORDBD"]}'}
    login = requests.post(apiurl, params=payload)
    print(login.text)
#def checkRegulamento(): 


@app.route('/bot', methods=['POST'])
def bot():
    resp = MessagingResponse()
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    #+19252915548
    resp = request.values.get('Body', '').lower()
    with open('tmp.tmp', 'w') as File:
        File.write(resp.lower())
    with open('tmp.tmp', 'r') as File:
        resp = File.read()
    os.remove("tmp.tmp")
    #return str(resp.lower())
    flag = True
    reg = False
    string = ""
    if not reg:
        string += "Regulamento"
        reg = True
        print(string)
        
            #message = client.messages.create(
    #                            body="Regulamento",
    #                            from_='whatsapp:+14155238886',
    #                            to='whatsapp:+351910663708'
    #                        )

    
    #message = client.messages.create(
    #                            body=request.values.get('Body', '').lower(),
    #                            from_='whatsapp:+14155238886',
    #                            to='whatsapp:+351910663708'
    #                        )
    
    #print(message.sid)

    # add webhook logic here and return a response
    return str(string)

@app.route('/api', methods=['POST'])
def api():
    return str("api")

if __name__ == '__main__':
    app.run()

# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
