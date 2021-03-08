from flask import Flask, request, jsonify
from conversation import findResponse
import mysql.connector
app = Flask(__name__)

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
        str_time = x[1].encode('UTF-8', 'ignore')
        str_userid = x[2].encode('UTF-8', 'ignore')
        str_query = x[3].encode('UTF-8', 'ignore')
        str_response = x[4].encode('UTF-8', 'ignore')
        dic['time'] = str_time
        dic['userid'] = str_userid
        dic['query'] = str_query
        dic['response'] = str_response
        chat_user.append(dic)

    cnx.close()
    return jsonify(chat_user)


@app.route('/users/<user>/query', methods=['POST'])
def userQuery(user):
    print('Printing post request', request)
    json = request.get_json()
    print('json:', json)
    str_userid = json['userid'].encode('UTF-8', 'ignore')
    str_query = json['query'].encode('UTF-8', 'ignore')
    str_time = json['time'].encode('UTF-8', 'ignore')
    print(str_query.decode("UTF-8"))
    print("MUDITITITITITI")
    str_response = findResponse(str_query.decode("UTF-8"))

    insertIntoDb(str_userid, str_query, str_time, str_response)

    return jsonify({'response': str_response})


@app.route('/test/response', methods=['POST'])
def testPost():
    print('Post req fetched : ', request)
    json = request.get_json()
    print('json:', json)
    return {'status': json['query']}


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


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000)
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
