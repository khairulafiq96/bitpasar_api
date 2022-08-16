from email import header, message
from urllib import response
from flask import Flask, request
import json
import psycopg2
import base64

app = Flask(__name__)

'''DATABASE_URL = os.environ['DATABASE_URL']'''

def initilizeConnection():
    print("Initializing connection")
    connection = psycopg2.connect("dbname=postgres user=postgres password=admin")
    cursor = connection.cursor()
    return connection, cursor

@app.before_request
def authHandler():
    header = request.headers
    try :
        if header['appKey'] == 'vlone':
            print("API call is verified")
            
    except Exception as E:
        if request.method == 'OPTIONS':
            print(request.method)
        else:
            return "",401
    

@app.after_request
def handlerCORS(response):
    if(request.method == 'GET' or request.method == 'OPTIONS' or request.method == 'POST' or request.method == 'DELETE'):
        print("OK")
        #response = flask.Response()
        response.headers["Status Code"] = "200 OK"
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Content-Type"] = "application/json"
        response.headers["Access-Control-Allow-Headers"] = "appKey,Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "*"     
        response.headers["Access-Control-Allow-Origin"] = "*"

        return response

@app.route('/myHello')
def hello():
    return 'Hello World'

@app.route('/registeruser',methods=['POST'])
def register():
    data = request.get_json()
    #print(data)
    connection, cursor  = initilizeConnection()
    userAccountInDB = verifyUserAccount(cursor,data['walletid'] )
    if userAccountInDB == 'True':
        cursor.execute("insert into bitpasar.users(name,email,phonenum,address1,address2,city,state,zipcode,walletid) values ('%s', '%s', '%s','%s','%s','%s','%s','%s','%s')"%(data['name'], data['email'], data['phonenum'], data['address1'], data['address2'], data['city'], data['state'], data['zipcode'], data['walletid']))
        connection.commit()
        cursor.execute("select * from bitpasar.users where walletid='%s'"% data['walletid'])
        response = cursor.fetchall()
        finalResp = {}
        for row in response:

                finalResp[row[0]]={}
                finalResp[row[0]]['name'] = row[1]
                finalResp[row[0]]['email'] = row[2]
                finalResp[row[0]]['phonenum'] = row[3]
                finalResp[row[0]]['address1'] = row[4]
                finalResp[row[0]]['address2'] = row[5]
                finalResp[row[0]]['city'] = row[6]
                finalResp[row[0]]['state'] = row[7]
                finalResp[row[0]]['zipcode'] = row[8]
                finalResp[row[0]]['walletid'] = row[9]
                

                #print (finalResp)
        return json.dumps(finalResp)
    else:
        message = {
            "status" : "denied",
            "message" : "The wallet is already created an account"
        }

        return json.dumps(message)

def verifyUserAccount(cursor,walletid):
    cursor.execute("select * from bitpasar.users where walletid='%s'"% walletid)
    response = cursor.fetchall()
    if response:
        '''This means that the User is in the DB'''
        return ("False")
    else:
        '''This means that the database is null'''
        return ("True")

@app.route('/addItem', methods=['POST'])
def addNewItem():
    data = request.get_json()
    connection, cursor  = initilizeConnection()

    '''Converting the long description to binary base64 for the bytea column in postgres, would reqquire refactoring'''
    longdesc64 = data['longdescription'].encode('utf-8')
    longdescencoded = base64.b64encode(longdesc64)
    longdescencoded = longdescencoded.decode('utf-8')

    '''To decode to text, just directly decode the string
        longdesc64 = data['longdescription'].encode('utf-8')
        longdescencoded = longdesc64.decode('utf-8')
    '''

    cursor.execute("""INSERT INTO bitpasar.items(ownerid, title, type, shortdescription, longdescription, itemprice, status, postagename, postageprice, images) VALUES ('%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', ARRAY %s)"""%(data['ownerid'],data['title'],data['type'],data['shortdescription'],longdescencoded,data['itemprice'],data['status'],data['postagename'],data['postageprice'],data['images'] ) )
    connection.commit()

    message = {
        "status" : "successful",
        "message" : "The item "+data['title']+" has been successfully added into the marketplace"
    }

    return json.dumps(message)

if __name__ == '__main__':
    app.run


