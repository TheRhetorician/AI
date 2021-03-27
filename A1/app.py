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
        str_contact1 = x[4].encode('UTF-8', 'ignore')
        str_contactnm1 = x[5].encode('UTF-8', 'ignore')
        str_contact2 = x[6].encode('UTF-8', 'ignore')
        str_contactnm2 = x[7].encode('UTF-8', 'ignore')
        str_contactdoc = x[8].encode('UTF-8', 'ignore')
        str_docname = x[9].encode('UTF-8', 'ignore')
        dic['userid'] = str_userid.decode("UTF-8")
        dic['password'] = str_password.decode("UTF-8")
        dic['name'] = str_name.decode("UTF-8")
        dic['address'] = str_address.decode("UTF-8")
        dic['contact1'] = str_contact1.decode("UTF-8")
        dic['contact name1'] = str_contactnm1.decode("UTF-8")
        dic['contact2'] = str_contact2.decode("UTF-8")
        dic['contact name2'] = str_contactnm2.decode("UTF-8")
        dic['doctor contact'] = str_contactdoc.decode("UTF-8")
        dic['doctor name'] = str_docname.decode("UTF-8")
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
    str_contact1 = json['contact1'].encode('UTF-8', 'ignore')
    str_contactnm1 = json['contact name1'].encode('UTF-8', 'ignore')
    str_contact2 = json['contact2'].encode('UTF-8', 'ignore')
    str_contactnm2 = json['contact name2'].encode('UTF-8', 'ignore')
    str_contactdoc = json['doctor contact'].encode('UTF-8', 'ignore')
    str_docname = json['doctor name'].encode('UTF-8', 'ignore')
    insertUser(str_userid, str_password, str_name, str_address, str_contact1,
               str_contactnm1, str_contact2, str_contactnm2, str_contactdoc, str_docname)

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
        contact1 = x[4]
        contactnm1 = x[5]
        contact2 = x[6]
        contactnm2 = x[7]
        contactdoc = x[8]
        docname = x[9]

    q_name = "name is " + str(name)
    q_address = "address is " + str(address)
    q_contact1 = "emergency contact is " + str(contact1)
    q_contactnm1 = "emergency contacts name is " + str(contactnm1)
    q_contact2 = "second emergency contact is " + str(contact2)
    q_contactnm2 = "second emergency contacts name is " + str(contactnm2)
    q_contactdoc = "doctors contact is " + str(contactdoc)
    q_docname = "doctors name is " + str(docname)
    print(name)
    print(findResponse(q_name))
    findResponse(q_address)
    findResponse(q_contact1)
    findResponse(q_contactnm1)
    findResponse(q_contact2)
    findResponse(q_contactnm2)
    findResponse(q_contactdoc)
    findResponse(q_docname)
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


def insertUser(user, password, name, address, contact1, contactnm1, contact2, contactnm2, contactdoc, docname):
    cnx = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database='user_chats', auth_plugin='mysql_native_password')
    mycursor = cnx.cursor()
    sql = "INSERT INTO users (userid,password,name,address,contact1,contactname1,contact2,contactname2,doctorcontact,doctorname) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (user, password, name, address, contact1, contactnm1,
           contact2, contactnm2, contactdoc, docname)
    mycursor.execute(sql, val)
    cnx.commit()
    cnx.close()


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
    cnx = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database='user_chats', auth_plugin='mysql_native_password')
    mycursor = cnx.cursor()

    cnx.close()
