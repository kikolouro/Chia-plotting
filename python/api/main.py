print(__name__)
try:
    from azure.storage.blob import BlobServiceClient    
    from azure.storage.blob import ContainerClient
    import os
    import requests
    from flask import Flask, request
    from decouple import config
except ImportError:
    print('Please install required modules: pip install -r requirements.txt')
    exit()
#print(config('STORAGE_ACC_ACCESS_KEY'))

credential = config('STORAGE_ACC_ACCESS_KEY')
service = BlobServiceClient(account_url="https://chiaplotsjoyn.blob.core.windows.net/", credential=credential)

container_client = ContainerClient.from_connection_string(conn_str=config('CONNECT_STRING'), container_name="teste2")

container_client.create_container()
print(container_client)
app = Flask(__name__)

@app.route('/createcontainer', methods=['GET'])
def createcontainer():
    try:
        container_client = ContainerClient.from_connection_string(conn_str=config('CONNECT_STRING'), container_name=request.args.get('container'))
        container_client.create_container()
    except Exception as ex:
        return str(ex)
    


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

