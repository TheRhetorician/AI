import os
from flask import Flask, render_template,url_for
from flask import request
from flask_cors import CORS
import json
from id_coord import makeDict
from preprocess_2 import preprocess
from q3_1 import calc

app = Flask(__name__)
CORS(app)
app.config["DEBUG"]= False

@app.route("/")
def index():
    '''
    Renders the starting query page.
    '''
    return render_template("index.html")   


@app.route('/getPath' , methods=['POST'])
def search():
    ''' 
    searches for path
    '''
    req_data = request.get_json()
    slat = req_data['slati']
    slon = req_data['slong']
    dlat = req_data['dlati']
    dlon = req_data['dlong']
    final_route = calc(slat, slon, dlat, dlon, node_coord, id_neigh) #calling the main function
    return {0:final_route}
    

if __name__ == "__main__":
    node_coord = makeDict()#id_coord
    id_neigh = preprocess()#preprocess_2
    app.run(host='0.0.0.0', port=3000, debug=False)