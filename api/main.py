try:
    import os
    import requests
    from flask import Flask, request
except ImportError:
    print('Please install required modules: pip install -r requirements.txt')
    exit()

app = Flask(__name__)


@app.route('/api', methods=['POST'])
def api():
    return str("api")

if __name__ == '__main__':
    app.run()

# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
