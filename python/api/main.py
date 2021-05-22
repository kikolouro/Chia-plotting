try:
    from azure.storage.blob import BlobServiceClient    
    from azure.storage.blob import ContainerClient
    import os
    import requests
    from azure.storage.blob import BlobClient
    from flask import Flask, request
    from decouple import config
except ImportError:
    print('Please install required modules: pip install -r requirements.txt')
    exit()
#print(config('STORAGE_ACC_ACCESS_KEY'))

credential = config('STORAGE_ACC_ACCESS_KEY')
service = BlobServiceClient(account_url="https://chiaplotsjoyn.blob.core.windows.net/", credential=credential)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.txt']
app.config['UPLOAD_FOLDER'] = 'plots'



@app.route('/createcontainer', methods=['GET'])
def createcontainer():
    try:
        container_client = ContainerClient.from_connection_string(conn_str=config('CONNECT_STRING'), container_name=request.args.get('container'))
        container_client.create_container()
        #return str(f"{request.args.get('container')} created")
        
    except Exception as ex:
        return str(ex)
        
@app.route('/uploadplot', methods=['POST'])
def uploadplot():
    plot = request.files['plot']
    if plot.filename != '':
        # SE CORRER NOUTRA MAQUINA
        plot.save(os.path.join(app.config['UPLOAD_FOLDER'], plot.filename)) 

        blob = BlobClient.from_connection_string(conn_str=config('CONNECT_STRING'), container_name="my_container", blob_name="my_blob")

        with open("./SampleSource.txt", "rb") as data:
            blob.upload_blob(data)
        return str("ficheiro guardado")
    return str("ficheiro nao guardado")

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

