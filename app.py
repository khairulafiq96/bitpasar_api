from email import header, message
from multiprocessing import connection
from sqlite3 import Cursor
from typing import final
from urllib import response
from flask import Flask, request
import json
import psycopg2
import base64
import math
import calendar
import pyrebase
import os

app = Flask(__name__)

'''DATABASE_URL = os.environ['DATABASE_URL']'''

firebaseConfig = {
    "apiKey": "AIzaSyDUnl86TI-bpWFD0NAaOrKTTm6msdmYvyU",
    "authDomain": "bitpasar.firebaseapp.com",
    "projectId": "bitpasar",
    "storageBucket": "bitpasar.appspot.com",
    "messagingSenderId": "782221905508",
    "appId": "1:782221905508:web:eed2befb480366548d1971",
    "databaseURL" : ""
}

def initilizeConnection():
    print("Initializing connection")
    connection = psycopg2.connect("dbname=postgres user=postgres password=admin")
    '''connection = psycopg2.connect(DATABASE_URL, sslmode='require')'''
    cursor = connection.cursor()
    return connection, cursor

def initializeFirebase():
    firebase = pyrebase.initialize_app(firebaseConfig)
    storage = firebase.storage()
    print("Firebase Storage is initialized")
    return storage

def convertUTC(dt):
    return calendar.timegm(dt.utctimetuple())

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

@app.route('/updateUserDetails',methods=['POST'])
def updateDetails():
    data = request.get_json()
    #print(data)
    connection, cursor  = initilizeConnection()
    cursor.execute("""UPDATE bitpasar.users
                    SET name='%s',email='%s',phonenum='%s',address1='%s',address2='%s',city='%s',state='%s',zipcode='%s'
                    WHERE walletid='%s';"""%(
                        data['name'], data['email'], data['phonenum'], data['address1'], data['address2'], 
                        data['city'], data['state'], data['zipcode'], data['walletid']))
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


@app.route('/getUserDetails',methods=['POST'])
def getUserDetails():
    data = request.get_json()
    #print(data)
    connection, cursor  = initilizeConnection()
    userAccountInDB = verifyUserAccount(cursor,data['walletid'] )
    print(userAccountInDB)
    if userAccountInDB == 'False':
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
            "status" : "unregistered",
            "message" : "Do update your contact details and address for autofill features. Update your details at the User Profile Page"
        }

        return json.dumps(message)

'''Verify the user in the database'''
def verifyUserAccount(cursor,walletid):
    cursor.execute("select * from bitpasar.users where walletid='%s'"% walletid)
    response = cursor.fetchall()
    if response:
        '''This means that the User is in the DB'''
        return ("False")
    else:
        '''This means that the database is null'''
        return ("True")

'''Add new item to the marketplace'''
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

    cursor.execute("""INSERT INTO bitpasar.items(ownerid, title, type, shortdescription, longdescription, itemprice, status, postagename, postageprice, images) VALUES ('%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', ARRAY %s)"""%(data['ownerid'],data['title'].lower(),data['type'].lower(),data['shortdescription'].lower(),longdescencoded,data['itemprice'],data['status'],data['postagename'],data['postageprice'],data['images'] ) )
    connection.commit()

    message = {
        "status" : "successful",
        "message" : "The item "+data['title']+" has been successfully added into the marketplace"
    }

    return json.dumps(message)

'''This route returns the all items and search results for the marketplace page, For All Items, search = null, this will not effect the LIKE statement'''
@app.route('/getFilteredMarketplace', methods=['POST'])
def getFilteredMarketplace():
    data = request.get_json()
    connection, cursor  = initilizeConnection()

    offsetVal = (int(data['page']) - 1) * 12
    cursor.execute("""SELECT * FROM bitpasar.items INNER JOIN bitpasar.users ON bitpasar.items.ownerid = bitpasar.users.id WHERE bitpasar.items.status = 'new' AND bitpasar.items.title LIKE '%%%s%%' ORDER BY bitpasar.items.timestamp DESC LIMIT 12 OFFSET %s"""%(data['search'],offsetVal))
    response = cursor.fetchall()
    finalResp =  {}
    for row in response:
        finalResp[row[0]] = {}
        finalResp[row[0]]['ownerid'] = row[1]
        finalResp[row[0]]['title'] = row[2]
        finalResp[row[0]]['type'] = row[3]
        finalResp[row[0]]['shortdescription'] = row[4]
        finalResp[row[0]]['itemprice'] = row[5]
        finalResp[row[0]]['status'] = row[6]
        finalResp[row[0]]['postagename'] = row[7]
        finalResp[row[0]]['postageprice'] = row[8]
        finalResp[row[0]]['images'] = row[9]
        finalResp[row[0]]['longdescription'] = decodeLongDescription(row[10])
        finalResp[row[0]]['timestamp'] = convertUTC(row[11])
        finalResp[row[0]]['ownername'] = row[13]
        finalResp[row[0]]['walletid'] = row[21]
        finalResp[row[0]]['phonenum'] = row[15]
        finalResp[row[0]]['location'] = row[19]


    return json.dumps(finalResp)

'''This route returns the individual item details based on the item id if called'''
@app.route('/getItemDetail', methods=['POST'])
def getIndividualItemDetail():
    data = request.get_json()
    connection, cursor  = initilizeConnection()
    cursor.execute("""SELECT * FROM bitpasar.items INNER JOIN bitpasar.users ON bitpasar.items.ownerid = bitpasar.users.id WHERE bitpasar.items.id = '%s' """%data['itemId'])
    response = cursor.fetchall()
    'print(response)'
    finalResp =  {}
    for row in response:
        finalResp[row[0]] = {}
        finalResp[row[0]]['ownerid'] = row[1]
        finalResp[row[0]]['title'] = row[2]
        finalResp[row[0]]['type'] = row[3]
        finalResp[row[0]]['shortdescription'] = row[4]
        finalResp[row[0]]['itemprice'] = row[5]
        finalResp[row[0]]['status'] = row[6]
        finalResp[row[0]]['postagename'] = row[7]
        finalResp[row[0]]['postageprice'] = row[8]
        finalResp[row[0]]['images'] = row[9]
        finalResp[row[0]]['longdescription'] = decodeLongDescription(row[10])
        finalResp[row[0]]['timestamp'] = convertUTC(row[11])
        finalResp[row[0]]['ownername'] = row[13]
        finalResp[row[0]]['walletid'] = row[21]
        finalResp[row[0]]['phonenum'] = row[15]
        finalResp[row[0]]['location'] = row[19]


    return json.dumps(finalResp)

'''Decoding to Base64, Highly inneficient, please refactor'''
def decodeLongDescription(memory):
    if(memory):
        longdescencoded = memory.tobytes()
        longdescencoded = base64.b64decode(longdescencoded)
        longdescencoded = longdescencoded.decode('utf-8')
        return longdescencoded

'''Calculate total pages needed for all of the items'''
'''This function only needs to be run once, to get the total number of page to be displayed'''
@app.route('/marketplacePageNum', methods=['POST'])
def calculateTotalPages():
    connection,cursor  = initilizeConnection()
    data = request.get_json()

    cursor.execute("""SELECT Count(*) FROM bitpasar.items WHERE status = 'new' AND title LIKE '%%%s%%' """%data['search'])
    '''Just getting one row of data'''
    rowcount = cursor.fetchone()[0]
    totalPages = math.ceil(rowcount/12)
    count = 1
    finalArr = []
    while count <= totalPages:
        finalArr.append(count)
        count += 1

    totalPages = {
        "totalPage" : finalArr
    }
    return json.dumps(totalPages)

@app.route('/createOrder',methods=['POST'])
def postCreateOrder():
    data = request.get_json()
    #print(data)
    connection, cursor  = initilizeConnection()

  
    cursor.execute('''INSERT INTO bitpasar.orders (
                        buyername, buyerwallet, ownername, ownerwallet, address1, address2, 
                        city, state, zipcode, postagename, postageprice, buyeremail, buyerphonenum, 
                        itemid, ownerid, buyerid, status) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')'''
                        %(data['buyername'], data['buyerwallet'], data['ownername'], data['ownerwallet'], data['address1'], data['address2'], 
                        data['city'], data['state'], data['zipcode'], data['postagename'], data['postageprice'], data['buyeremail'], 
                        data['buyerphonenum'], data['itemid'], data['ownerid'], data['buyerid'], data['status']))
    connection.commit()

    message = {
    "status" : "successful",
    "message" : "The item has been successfully paid. Please download your receipt for future reference. The seller has been notified to ship your item"
    }
    
    return json.dumps(message)

@app.route('/getUserPurchases',methods=['POST'])
def userPurchase():
    data = request.get_json()
    #print(data)
    connection, cursor  = initilizeConnection()
    cursor.execute("""SELECT orders.id,items.title, items.shortdescription, items.itemprice, orders.status, items.images, orders.timestamp, orders.postagename, orders.postageprice, orders.trackerid, users.name as ownername, users.phonenum, users.walletid
                        FROM bitpasar.items AS items 
                        JOIN bitpasar.orders AS orders ON items.id = orders.itemid
                        JOIN bitpasar.users AS users ON items.ownerid = users.id
                        WHERE orders.buyerwallet = '%s'"""%data['walletid'])
    response = cursor.fetchall()
    finalResp = {}
    for row in response:
            finalResp[row[0]] = {}
            finalResp[row[0]]['title'] = row[1]
            finalResp[row[0]]['shortdescription'] = row[2]
            finalResp[row[0]]['itemprice'] = row[3]
            finalResp[row[0]]['status'] = row[4]
            finalResp[row[0]]['images'] = row[5][0]
            finalResp[row[0]]['timestamp'] = convertUTC(row[6])
            finalResp[row[0]]['postagename'] = row[7]
            finalResp[row[0]]['postageprice'] = row[8]
            finalResp[row[0]]['trackerid'] = row[9]
            finalResp[row[0]]['ownername'] = row[10]
            finalResp[row[0]]['ownerphonenum'] = row[11]
            finalResp[row[0]]['ownerwallet'] = row[12]
            
            #print (finalResp)
    return json.dumps(finalResp)

'''This endpoint returns all of the orders to ship and shipped out orders , getAllOrders'''
@app.route('/getAllOrders',methods=['POST'])
def userAllOrders():
    data = request.get_json()
    #print(data)
    connection, cursor  = initilizeConnection()
    cursor.execute("""SELECT orders.id,items.title, items.shortdescription,items.itemprice,orders.status,items.images,orders.timestamp,
                    orders.buyername as buyername, orders.buyerphonenum, orders.buyerwallet, orders.address1, orders.address2, 
                    orders.city, orders.state, orders.zipcode, orders.postagename, orders.postageprice, orders.trackerid
                    FROM bitpasar.items AS items 
                    JOIN bitpasar.orders AS orders ON items.id = orders.itemid
                    WHERE orders.ownerid = '%s'"""%data['ownerid'])
    response = cursor.fetchall()
    finalResp = {}
    for row in response:
            finalResp[row[0]] = {}
            finalResp[row[0]]['title'] = row[1]
            finalResp[row[0]]['shortdescription'] = row[2]
            finalResp[row[0]]['itemprice'] = row[3]
            finalResp[row[0]]['status'] = row[4]
            finalResp[row[0]]['images'] = row[5][0]
            finalResp[row[0]]['timestamp'] = convertUTC(row[6])
            finalResp[row[0]]['buyername'] = row[7]
            finalResp[row[0]]['buyerphonenum'] = row[8]
            finalResp[row[0]]['buyerwallet'] = row[9]
            finalResp[row[0]]['address1'] = row[10]
            finalResp[row[0]]['address2'] = row[11]
            finalResp[row[0]]['city'] = row[12]
            finalResp[row[0]]['state'] = row[13]
            finalResp[row[0]]['zipcode'] = row[14]
            finalResp[row[0]]['postagename'] = row[15]
            finalResp[row[0]]['postageprice'] = row[16]
            finalResp[row[0]]['trackerid'] = row[17]
            
            #print (finalResp)
    return json.dumps(finalResp)

@app.route('/updateOrderTracker',methods=['POST'])
def updateOrderTracker():
    data = request.get_json()
    #print(data)
    connection, cursor  = initilizeConnection()
    cursor.execute("""UPDATE bitpasar.orders SET 
                      status='shipped' , trackerid='%s' WHERE id = '%s'"""%(
                        data['trackerid'], data['orderid']))
    connection.commit()

    finalResp = {}

    '''Checking if the cursor did not updated any of the rows'''
    if (cursor.rowcount != 0):  
        finalResp = {data['orderid'] : {
                                        "status" : "shipped",
                                        "trackerid" : data['trackerid']
                    }}
    else:
        finalResp = {
            "status" : "unsuccessful",
            "message" : "Unable to update the tracking number, please reach out to the developer"
        }

    return json.dumps(finalResp)

@app.route('/getAllAds',methods=['POST'])
def userAllAds():
    data = request.get_json()
    #print(data)
    connection, cursor  = initilizeConnection()
    cursor.execute("""SELECT * FROM bitpasar.items WHERE ownerid = '%s'"""%(
                        data['ownerid']))
    response = cursor.fetchall()
    finalResp = {}
    for row in response:
        finalResp[row[0]] = {}
        finalResp[row[0]]['ownerid'] = row[1]
        finalResp[row[0]]['title'] = row[2]
        finalResp[row[0]]['type'] = row[3]
        finalResp[row[0]]['shortdescription'] = row[4]
        finalResp[row[0]]['itemprice'] = row[5]
        finalResp[row[0]]['status'] = row[6]
        finalResp[row[0]]['postagename'] = row[7]
        finalResp[row[0]]['postageprice'] = row[8]
        finalResp[row[0]]['images'] = row[9]
        finalResp[row[0]]['longdescription'] = decodeLongDescription(row[10])
        finalResp[row[0]]['timestamp'] = convertUTC(row[11])
            
            #print (finalResp)
    return json.dumps(finalResp)

@app.route('/deleteAds',methods=['DELETE'])
def deleteUserAds():
    data = request.get_json()
    #print(data)
    connection, cursor  = initilizeConnection()
    cursor.execute("""DELETE FROM bitpasar.items WHERE id = '%s' """
                  %(data['id']))
    connection.commit()

    if (cursor.rowcount != 0):  
         finalResp = {
            "status" : "successful",
            "message" : "Item has been successfully deleted"
        }
    else:
        finalResp = {
            "status" : "unsuccessful",
            "message" : "Unable to update the tracking number, please reach out to the developer"
        }

    return json.dumps(finalResp)


'''
Before developing the future enhancement, 
the structure of the of the storage would be : 
images/{itemid}/images_name.jpg

This would improve on effeciency as firebase.listAll will be calling
all of the images path/name

This would effect a lot of the variables in the React code.

Future enchancement : 
To ensure all of the images stored in firebase are deleted correctly,
1. List all of the image path from DB
2. Get all of the images path and name from Firebase
3. Compare between the database path from DB and Firebase
4. Only matching values will be deleted
5. If the deletion failed, break the code and return as status failed
6. If all of the deletion of images are successful, the code proceeds to
delete the user data in the db
'''

@app.route('/deleteUser',methods=['DELETE'])
def userDeletion():
    data = request.get_json()
    storage = initializeFirebase()
    connection, cursor = initilizeConnection()
    cursor.execute('''
                    SELECT images from bitpasar.items WHERE ownerid = 'TEST'
                    ''')
    response = cursor.fetchall()
    finalResp = {}
    '''As the column is an array, a nested loop is required to extract the individual URL'''
    for row in response:
        for url in row:
            for indvURL in url:
                '''Presumably all of the firebase deletion will be successful for alpha'''
                firebaseDeletion(storage,indvURL)
    cursor.execute('''DELETE FROM bitpasar.users WHERE id = '%s' '''%data['userid'])
    connection.commit()

    if (cursor.rowcount != 0):  
         finalResp = {
            "status" : "successful",
            "message" : "User has been successfull deleted"
        }
    else:
        finalResp = {
            "status" : "unsuccessful",
            "message" : "An error occurred, please reach out to the developer"
        }
    return json.dumps(finalResp)

def firebaseDeletion(storage,url):
    try :
        storage.delete(decodeURItoFirebasePath(url),"")
        print("Successful deletion of :" + decodeURItoFirebasePath(url))
        return "success"
    except Exception as e :
        print(e)
        return "failed"

'''Had to convert JS to Python based on this guide
https://stackoverflow.com/questions/56762486/how-to-get-the-firebase-storage-path-from-the-the-storage-url'''
'''This function converts URL to readable Firebase Path format'''
def decodeURItoFirebasePath(url):
    url_token = url.split('?')
    my_url = url_token[0].split('/')
    return my_url[len(my_url) - 1].replace("%2F", "/")

if __name__ == '__main__':
    app.run


