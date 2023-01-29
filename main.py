from flask import Flask, jsonify, request
import os

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})
    
    
@app.route('/receive_msg', methods=['POST','GET'])
def webhook():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token")== "Saksham":
            return "Verification token missmatch", 403
        return request.args['hub.challenge'], 200
    return "Hello world", 200


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
