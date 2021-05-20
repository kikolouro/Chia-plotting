print(__name__)
try:
    import os
    import requests
    from flask import Flask, request
except ImportError:
    print('Please install required modules: pip install -r requirements.txt')
    exit()

nrvisitas = 0
app = Flask(__name__)

@app.route('/')
def Main():
    return 'Welcome to the Test API!'

@app.route('/teste', methods=['POST'])
def teste():
    print("teste")
    return str("teste")

@app.route('/api')
def api():
    print("api")
    return str("api")

if __name__ == "main":
    app.run(host='0.0.0.0')

