try:
    import azure.storage.blob
    from azure.storage.blob import BlobServiceClient
    from azure.storage.blob import ContainerClient, BlobSasPermissions
    import os
    import json
    from datetime import datetime, timedelta
    from azure.storage.blob import BlobClient
    from flask import Flask, request
    import bcrypt
    from decouple import config
    import mysql.connector
    from flask_cors import CORS
    import re
except ImportError:
    print('Please install required modules: pip install -r requirements.txt')
    exit()
# https://zetcode.com/python/bcrypt/ --- bcrypt

credential = config('STORAGE_ACC_ACCESS_KEY')
service = BlobServiceClient(account_url=f"https://{config('STORAGE_ACC_NAME')}.blob.core.windows.net/", credential=credential)

mydb = mysql.connector.connect(
    host="mysql",
    user="root",
    password=f"{config('DB_ROOT_PASSWORD')}",
    database=f"{config('DB_NAME')}"
)
mycursor = mydb.cursor()


app = Flask(__name__)
CORS(app)

app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.txt']
app.config['UPLOAD_FOLDER'] = 'plots'


def hashpw(password):
    salt = bcrypt.gensalt()
    pw = bcrypt.hashpw(password, salt)
    return pw


def checkemail(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if(re.search(regex, email)):
        return True
    else:
        return False


def samepw(pwbd, pwuser):
    pw = hashpw(pwuser)
    if bcrypt.checkpw(pwbd, pw):
        return True
    else:
        return False

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    #sreturn str(mycursor)
    password = request.form.get('password').encode('utf-8')
    if checkemail(email):
        pw = hashpw(password)
        sql = f"INSERT INTO users(email, password) VALUES (%s, %s)"
        val = (email, pw.decode('utf8'))
        mycursor.execute(sql, val)

        mydb.commit()
        code = {
            "code": "1",
            "message": "Register completed"
        }
    else:
        code = {
            "code": "0",
            "message": "Register incomplete, bad email"
        }
    return json.dumps(code) 

@app.route('/login', methods=["POST"])
def login():
    if checkemail(request.form.get('email')):
        sql = f"Select * from users where email like '{request.form.get('email')}'"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        return str(result)
        #if samepw(request.form.get('loginPassword').encode('uft8'), result[0][3]):
    else:
        code = {
            "code": "0",
            "message": "Register incomplete, bad email"
        }


@app.route('/createcontainer', methods=['GET'])
def createcontainer():
    try:
        container_client = ContainerClient.from_connection_string(conn_str=config(
            'CONNECT_STRING'), container_name=request.args.get('container'))
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
        blob = BlobClient.from_connection_string(conn_str=config(
            'CONNECT_STRING'), container_name=request.form.get('container'), blob_name=plot.filename)

        with open(os.path.join(app.config['UPLOAD_FOLDER'], plot.filename), "rb") as data:
            blob.upload_blob(data)
        return str("ficheiro guardado")
    return str("ficheiro nao guardado")


@app.route('/generateploturl', methods=['GET'])
def generateploturl():
    expiry = datetime.utcnow() + timedelta(days=3)
    sasToken = azure.storage.blob.generate_blob_sas(f"{config('STORAGE_ACC_NAME')}", request.args.get('container'), request.args.get('blob'), snapshot=None, account_key=config('STORAGE_ACC_ACCESS_KEY'), user_delegation_key=None, permission=BlobSasPermissions(
        read=True, add=False, create=False, write=False, delete=False, delete_previous_version=False, tag=False), expiry=expiry, start=datetime.utcnow(), policy_id=None, ip=None,)

    return str(f"https://{config('STORAGE_ACC_NAME')}.blob.core.windows.net/{request.args.get('container')}/{request.args.get('blob')}?{sasToken}")


