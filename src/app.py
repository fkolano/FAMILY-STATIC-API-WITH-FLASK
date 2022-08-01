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

        "family": members
    }

    return jsonify(response_body), 200


@app.route('/member/<int:member_id>', methods=['GET'])
def handle_get_member(member_id):
    status = 200
    try:
        result = jackson_family.get_member(member_id)
        if result == False:
            response_body = {"message": "Member not found"}
            status = 404
        else:
            response_body = {"message":  "Member was successfully retrieved", "member": result}

    except:
        response_body = {
            "message":  "There was a problem on the server, could not fulfill request"}
        status = 500

    return jsonify(response_body), status


# this is the beiginning
# I understand the method but how did we add member again since we did not use the member_id?
@app.route('/add_member', methods=['POST'])
def handle_add_member():
    body = request.json

    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.add_member(body)
    response_body = {

        "members": members
    }

    return jsonify(response_body), 200


# this is the beiginning
@app.route('/member/<int:member_id>', methods=['DELETE'])
def handle_delete_member(member_id):
    status = 200
    try:
        result = jackson_family.delete_member(member_id)
        if result == False:
            response_body = {"message": "Member not found"}
            status = 404
        else:
            response_body = {"message":  "Member was successfully deleted"}

    except:
        response_body = {
            "message":  "There was a problem on the server, could not fulfill request"}
        status = 500

    return jsonify(response_body), status


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
