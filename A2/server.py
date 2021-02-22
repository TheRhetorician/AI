import os
from flask import Flask, render_template,url_for
from flask import request

app = Flask(__name__)
app.config["DEBUG"]= True


@app.route("/")
def index():
    '''
    Renders the starting query page.
    '''
    return render_template("index.html")   


@app.route('/search' , methods=['POST'])
def search():
    ''' 
    Function to be called after query is inserted to return the results.
    Data structure used includes dictionary and lists.
    Renders the final ranked documents.
    '''
    printf("Here is the response")
    return render_template("index.html") 
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)

#  ,docs=[["Movie 1","Some year", "something else","another attribute"]]