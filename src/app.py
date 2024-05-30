"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

jackson_family.add_member(
    {
    'first_name': 'John',
    'age': 33,
    'lucky_numbers': [7, 13, 22]

    }
)

jackson_family.add_member(
    {
    'first_name': 'Jane',
    'age': 35,
    'lucky_numbers': [10, 14, 3]

    }
)

jackson_family.add_member(
    {
    'first_name': 'Jimmy',
    'age': 5,
    'lucky_numbers': [1]

   }
)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(response_body['family']), 200

@app.route('/members', methods=['POST'])
def add_new_member():
    #converting the request coming in from HTTP from text to Json format
    new_family_member = request.json

    #adding the new member to the family
    jackson_family.add_member(new_family_member)
    
    #display all the members in JSON format confirming that
    #the new member was added
    members = jackson_family.get_all_members()
    response_body = {
        "results": members
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
