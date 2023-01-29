from flask import Flask, request
import requests
from helper import *
 
app = Flask(__name__)
 
@app.route('/')
def index():
    return "Hello"

 
@app.route('/receive_msg', methods=['POST','GET'])
def webhook():
    res = request.get_json()
    print('Input---------', res)
    
    msg = 'Error in Processing!'
    
    try:
        print('Entering Try Block')
        status = processRequest(res)            
    except:
        print('Entering Except Block')
        pass
    
    print('--------------------------------------------------------------------------')
    return '200 OK HTTPS.'


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
