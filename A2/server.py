import os
from flask import Flask, render_template,url_for
from flask import request
from flask_cors import CORS
import json

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
    print("Here is the response")
    print(num)
    return render_template("index.html") 
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)

#  ,docs=[["Movie 1","Some year", "something else","another attribute"]]