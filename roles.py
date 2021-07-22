from flask import Flask, Blueprint, session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import abort, url_for, Api, Resource, request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/users.db'
app.config['SECRET_KEY'] = 'This15NiCe'
db = SQLAlchemy(app)
api_bp = Blueprint("api", __name__)
api =  Api(api_bp)

@api.blueprint.route("/")
def home():
    message = "This is home"
    return {"message":message}, 200
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_active =db.Boolean()
    is_admin = db.Boolean()

db.create_all()

class Register(Resource):
    def post(self):
        user = request.json["user"]
        passwd = request.json["passwd"]
        is_active = request.json["is_active"]
        is_admin = request.json["is_admin"]
        data = Users(username=user, password=passwd, is_active=is_active, is_admin=is_admin)
        if user is None or passwd is None:
            message = "You have to insert a username"
            return { "error": message }, 400
        elif Users.query.filter_by(username=user).first() is not None:
            message = "User already added"
            return {"error":message}, 401
        else:
            db.session.add(data)
            db.session.commit()
            message = "Success!!"
        return {"message":message}, 201

api.add_resource(Register, "/reg", methods=["POST"])
class Login(Resource):
    def post(self):
        username = request.json["user"]
        password = request.json["passwd"]
        user = Users.query.filter_by(username=username).first()
        if username is None or password is None:
            message = "Either username or password is missing"
            return {"message":message}, 400
        elif user.password != password:
            message = "Incorrect username or password"
            return {"message":message}, 400
        else:
            session['username'] = user.username
            message = "You have successfully logged in"
        return ({"session":session.get("username")}, {"message":message}), 200
api.add_resource(Login, "/login", methods=["POST"])

class Modify(Resource):
    """modify data from db"""
    def put(self):
        pass
    def delete(self):
        pass
#@api.add_resource(Modify, "/mod", methods=["PUT", "DELETE"])

class Logout(Resource):
    def post(self):
        user = session.get("username")
        if user is None:
            error = "You have already logged out"
            return {"error": error}, 400
        session.clear()
        message = "You have successfully logged out"
        return {"message": message}, 200
api.add_resource(Logout, "/logout", methods=["POST"])

app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run(port=5008, debug=True)
