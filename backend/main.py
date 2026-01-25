from flask import Flask
import os
from applications.models import *
from flask_restful import Api
from applications.api import WelcomeApi, LoginApi, SignupApi

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(base_dir, "grocerry.sqlite3")
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///grocerry.sqlite3"

api = Api(app)
db.init_app(app)
app.app_context().push()

def add_admin():
    admin = Users.query.filter_by(role = "admin").first()
    if not admin:
        admin = Users(name = "Admin", email = "admin@gs.com", password = "2026", role = "admin")
        db.session.add(admin)
        db.session.commit()
        return "Admin Added"

api.add_resource(WelcomeApi, '/api/welcome')
api.add_resource(LoginApi, '/api/login')
api.add_resource(SignupApi, '/api/signup')

if __name__ == "__main__":
    db.create_all()
    add_admin()
    app.run(debug=True)

