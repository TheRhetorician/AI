import os
from flask import Flask, render_template,url_for
from flask import request
from flask_cors import CORS
import json
from q2 import cal

app = Flask(__name__)
CORS(app)
app.config["DEBUG"]= True


@app.route("/")
def index():
    '''
    Renders the starting query page.
    '''
    return render_template("index.html")   


@app.route('/getSolution' , methods=['POST'])
def search():
    ''' 
    '''
    req_data = request.get_json()
    print(req_data)
    num = json.loads(req_data['number'])
    values =req_data['values']
    print("Here is the response")
    print(num)
    print(values)
    num_west={}
    for i in range(num):
        num_west[i+1]=int(values[i])
    ans=cal(num,num_west)
    fin_ans={}
    for i in range(len(ans)):
        fin_ans[i]=ans[i]
    return {0:fin_ans,1:len(ans)}
    

if __name__ == "__main__":
    app.run(debug=True)
