import functools
import json
from flask import Flask, Blueprint, session
from flask_restful import request, Api, abort, Resource, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] ="THUgLif3"
api_bp =  Blueprint("api", __name__)
api = Api(api_bp)

"""
Below uses default config;
spaces -> 4

@api.representation("application/json")
def out_json(data, code, headers=None):
    resp = api.make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp
"""

@api.blueprint.before_app_request
def before():
    user = session.get("user")
    if user is None:
        session["user"] = "Guest"

def data_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        info_ = session.get("data")
        if info_ is None:
            abort(401)
        return view(**kwargs)
    return wrapped_view

@api.blueprint.route("/")
def get_data():
    data = {"name": "Collins"}
    if session.get("user") == "Guest":
        info = {"name":"Collins", "age": 21}
        print(json.dumps(info))
    return {"data":data, "info": info} , 200

@api.blueprint.route("/home/<string:message>",methods=["GET", "POST", "PUT", "HEAD"])
def home(message):
    return {"message":message}, 200

@api.blueprint.route("/red/", methods=["GET"])
def redr():
    return url_for("api.red"), 302

@api.blueprint.route("/redr", methods=["GET"])
def red():
    message = "I am legend"
    return {"message": message}, 200

class AddData(Resource):
    def post(self):
        data = request.json["data"]
        session["data"] = data
        return {"data": data}, 201

api.add_resource(AddData, "/", methods=["POST"])

datamodel = {"name":"Collins"}
class DataModel(Resource):
    method_decorators = [data_required]

    def get(self):
        print(session)
        return datamodel, 200

    def post(self):
        age = request.json["age"]
        datamodel["age"] = age
        print(session)
        return ({"data": datamodel},{"newdata":{"age": age}}), 201

    def put(self):
        name = request.json["name"]
        age = request.json["age"]
        datamodel["name"] = name
        datamodel["age"] = age
        print(session)
        return {"datamodel": datamodel}, 201

    def delete(self):
        print(session)
        session.clear()
        datamodel.clear()
        return "", 204

api.add_resource(DataModel, "/data")
app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run(port=5007, debug=True)

"""
blueprints
decorators
use json output
"""
