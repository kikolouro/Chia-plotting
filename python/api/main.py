try:
    import azure.storage.blob
    from azure.storage.blob import BlobServiceClient    
    from azure.storage.blob import ContainerClient, BlobSasPermissions
    import os
    from datetime import datetime, timedelta
    from azure.storage.blob import BlobClient
    from flask import Flask, request
    from decouple import config
    import mysql.connector
    from flask_cors import CORS
except ImportError:
    print('Please install required modules: pip install -r requirements.txt')
    exit()
#print(config('STORAGE_ACC_ACCESS_KEY'))

credential = config('STORAGE_ACC_ACCESS_KEY')
service = BlobServiceClient(account_url="https://chiaplotsjoyn.blob.core.windows.net/", credential=credential)

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.txt']
app.config['UPLOAD_FOLDER'] = 'plots'


@app.route('/register', methods=['POST'])
def register():
    mydb = mysql.connector.connect(
            host="mysql",
            user="root",
            password=f"{config('DB_ROOT_PASSWORD')}",
            database=f"{config('DB_NAME')}"
            )
    mycursor = mydb.cursor()
    print(request.form)
    return str(request.form)

@app.route('/createcontainer', methods=['GET'])
def createcontainer():
    try:
        container_client = ContainerClient.from_connection_string(conn_str=config('CONNECT_STRING'), container_name=request.args.get('container'))
        container_client.create_container()
        return str(f"{request.args.get('container')} created")
        
    except Exception as ex:
        return str(ex)
        
@app.route('/uploadplot', methods=['POST'])
def uploadplot():
    plot = request.files['plot']
    if plot.filename != '':
        # SE CORRER NOUTRA MAQUINA
        plot.save(os.path.join(app.config['UPLOAD_FOLDER'], plot.filename)) 
        blob = BlobClient.from_connection_string(conn_str=config('CONNECT_STRING'), container_name=request.form.get('container'), blob_name=plot.filename)

        with open(os.path.join(app.config['UPLOAD_FOLDER'], plot.filename), "rb") as data:
            blob.upload_blob(data)
        return str("ficheiro guardado")
    return str("ficheiro nao guardado")

@app.route('/generateploturl', methods=['GET'])
def generateploturl():
    expiry= datetime.utcnow() + timedelta(days=3)
    sasToken = azure.storage.blob.generate_blob_sas("chiaplotsjoyn", request.args.get('container'), request.args.get('blob'), snapshot=None, account_key=config('STORAGE_ACC_ACCESS_KEY'), user_delegation_key=None, permission=BlobSasPermissions(read=True, add=False, create=False, write=False, delete=False, delete_previous_version=False, tag=False), expiry=expiry, start=datetime.utcnow(), policy_id=None, ip=None,)
    
    return str(f"https://chiaplotsjoyn.blob.core.windows.net/{request.args.get('container')}/{request.args.get('blob')}?{sasToken}")


if __name__ == "main":
    app.run(host='0.0.0.0')

