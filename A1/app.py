from flask import Flask, request, jsonify
from conversation import findResponse, learn
import mysql.connector
app = Flask(__name__)
app.config["DEBUG"] = True

# TODO increase size of sql table columns


@app.route("/")
def index():
    return {"This is index page": "s"}


@app.route("/users/<user>")
def userGet(user):
    print('testing get req')
    cnx = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database='user_chats', auth_plugin='mysql_native_password')
    # a database cursor is a control structure that enables traversal over the records in a database
    mycursor = cnx.cursor()
    a = user
    val = (a,)

    mycursor.execute("SELECT * FROM chats WHERE userid=%s", val)
    myresult = mycursor.fetchall()
    chat_user = []

    for x in myresult:
        dic = {}
        print(x)
        str_time = x[1].encode('UTF-8', 'ignore')
        str_userid = x[2].encode('UTF-8', 'ignore')
        str_query = x[3].encode('UTF-8', 'ignore')
        str_response = x[4].encode('UTF-8', 'ignore')
        # print(type(str_time))
        dic['time'] = str_time.decode("UTF-8")
        dic['userid'] = str_userid.decode("UTF-8")
        dic['query'] = str_query.decode("UTF-8")
        dic['response'] = str_response.decode("UTF-8")
        chat_user.append(dic)
        # learn()

    cnx.close()
    return jsonify(chat_user)


@app.route("/users/<user>/details")
def userDetailsGet(user):
    cnx = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database='user_chats', auth_plugin='mysql_native_password')
    # a database cursor is a control structure that enables traversal over the records in a database
    mycursor = cnx.cursor()
    a = user
    val = (a,)

    mycursor.execute("SELECT * FROM users WHERE userid=%s", val)
    myresult = mycursor.fetchall()
    chat_user = []
    for x in myresult:
        dic = {}
        str_userid = x[0].encode('UTF-8', 'ignore')
        str_password = x[1].encode('UTF-8', 'ignore')
        str_name = x[2].encode('UTF-8', 'ignore')
        str_address = x[3].encode('UTF-8', 'ignore')
        str_contact = x[4].encode('UTF-8', 'ignore')
        dic['userid'] = str_userid.decode("UTF-8")
        dic['password'] = str_password.decode("UTF-8")
        dic['name'] = str_name.decode("UTF-8")
        dic['address'] = str_address.decode("UTF-8")
        dic['contact'] = str_contact.decode("UTF-8")
        chat_user.append(dic)
        print(dic)
    cnx.close()
    return jsonify(chat_user)


@app.route('/users/<user>/details', methods=['POST'])
def userDetailsPost(user):
    print('Printing post request', request)
    json = request.get_json()
    print('json:', json)
    str_userid = json['userid'].encode('UTF-8', 'ignore')
    str_password = json['password'].encode('UTF-8', 'ignore')
    str_name = json['name'].encode('UTF-8', 'ignore')
    str_address = json['address'].encode('UTF-8', 'ignore')
    str_contact = json['contact'].encode('UTF-8', 'ignore')
    insertUser(str_userid, str_password, str_name, str_address, str_contact)

    return jsonify({'response': "added"})


@app.route('/users/<user>/query', methods=['POST'])
def userQuery(user):
    print('Printing post request', request)
    json = request.get_json()
    print(type(json['query']))
    str_userid = json['userid'].encode('UTF-8', 'ignore')
    str_query = json['query'].encode('UTF-8', 'ignore')
    print("\n\n", str_query)
    print(type(json['query']))
    str_userid = json['userid'].encode('UTF-8', 'ignore')
    str_query = json['query'].encode('UTF-8', 'ignore')
    print("\n\n", str_query)
    str_time = json['time'].encode('UTF-8', 'ignore')
    print(str_query.decode("UTF-8"))
    # learn()
    str_response = findResponse(str_query.decode("UTF-8"))

    insertIntoDb(str_userid, str_query, str_time, str_response)

    return jsonify({'response': str_response})


@app.route('/test/response', methods=['POST'])
def testPost():
    print('Post req fetched : ', request)
    json = request.get_json()
    print('json:', json)
    return {'status': json['query']}


@app.route('/learn', methods=['POST'])
def postman_learn():
    learn()
    req_data = request.get_json()
    user = req_data['userid']
    cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1',
                                  database='user_chats', auth_plugin='mysql_native_password')
    # a database cursor is a control structure that enables traversal over the records in a database
    mycursor = cnx.cursor()
    a = user
    val = (a,)

    mycursor.execute("SELECT * FROM users WHERE userid=%s", val)
    myresult = mycursor.fetchall()
    for x in myresult:
        name = x[2]
        address = x[3]
        contact = x[4]

    q_name = "name is " + str(name)
    q_address = "address is " + str(address)
    q_contact = "emergency contact is " + str(contact)
    print(name)
    print(findResponse(q_name))
    findResponse(q_address)
    findResponse(q_contact)
    return jsonify({"done": "done"})


@app.route('/test/response')
def test():
    return {"abc": "def",
            "asd": "asdfg"
            }


def insertIntoDb(user, query, time1, response):
    cnx = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database='user_chats', auth_plugin='mysql_native_password')
    mycursor = cnx.cursor()
    sql = "INSERT INTO chats (time,userid,query,response) VALUES (%s,%s,%s,%s)"
    val = (time1, user, query, response)
    mycursor.execute(sql, val)
    cnx.commit()
    cnx.close()


def insertUser(user, password, name, address, contact):
    cnx = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database='user_chats', auth_plugin='mysql_native_password')
    mycursor = cnx.cursor()
    sql = "INSERT INTO users (userid,password,name,address,emergency_contact) VALUES (%s,%s,%s,%s,%s)"
    val = (user, password, name, address, contact)
    mycursor.execute(sql, val)
    cnx.commit()
    cnx.close()


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
    cnx = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database='user_chats', auth_plugin='mysql_native_password')
    mycursor = cnx.cursor()
    #mycursor.execute("create table customers(name VARCHAR(255))")

    '''
    code for inserting into db
    '''
    # sql = "INSERT INTO chats (time,userid,query,response) VALUES (%s,%s,%s,%s)"
    # val = ("24/3","smit","insert from code","hope it works!");
    # mycursor.execute(sql,val)
    # cnx.commit()
    # print(mycursor.rowcount,"record inserted")

    ''''
    code for fetching from db
    '''
    # a="smit"
    # val=(a,)
    # mycursor.execute("SELECT * FROM chats WHERE userid=%s",val)
    # myresult = mycursor.fetchall()
    # chat_user=[]
    # for x in myresult:
    #     str_time = x[1].encode('UTF-8','ignore')
    #     str_userid = x[2].encode('UTF-8','ignore')
    #     str_query = x[3].encode('UTF-8','ignore')
    #     str_response = x[4].encode('UTF-8','ignore')
    #     chat_user.append([str_time,str_userid,str_query,str_response])
    #     print(type(x[2]))
    # print(chat_user)

    cnx.close()
