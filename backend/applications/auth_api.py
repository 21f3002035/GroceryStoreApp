from flask import request, current_app as app
from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt

from .models import *

class LoginApi(Resource):
    def post(self):
        data = request.json
        
        if not (data.get("email") and data.get("password")):
            return {"message" : "Both email and password fields are required."}, 400
        
        user = Users.query.filter_by(email = data.get("email")).first()

        if not user:
            return {"message" : "User not found."}, 404 # not found
        
        if user.password != data.get("password"):
            return {"message" : "Incorrect Password."}, 400 # bad request
        
        if user.role == "manager" and user.status == "pending":
            return {"message" : "Your account status is pending."}
        
        # token = create_access_token({"role" : user.role, "user_id" : user.id})
        token = create_access_token(
                                    identity=str(user.id), 
                                    additional_claims={"role": user.role}
                                    )
        return {
                "message" : "User logged in successfully.",
                "token" : token,
                "user_name" : user.name,
                "user_role" : user.role
                }, 200 # success
        
               
        
class SignupApi(Resource):
    def post(self):
        data = request.json
        if not (data.get("name") and data.get("email") and data.get("password")):
            
            return {"message" : "Bad Request!! All fields are required."}, 400    
        
        if len(data.get("name").strip()) > 60 or len(data.get("name").strip()) < 4:
            return {"message" : "Length of name must between 4 and 60 char."}, 400
        
        if len(data.get("email").strip()) > 100 or len(data.get("email").strip()) < 5:
            return {"message" : "Length of email must between 5 and 100 char."}, 400
        
        if len(data.get("password").strip()) > 60 or len(data.get("password").strip()) < 5:
            return {"message" : "Length of password must between 5 and 60 char."}, 400
        
        if data.get("role") not in ["customer", "manager"]:
            return {"message" : "Enter a valid role"}, 400

        user = Users.query.filter_by(email = data.get("email")).first()
        if user:
            return {"message":"user already exists!"}, 400
        
        new_user = Users(name = data.get('name').strip(), email = data.get('email').strip(), 
                        password = data.get('password').strip(), role = data.get('role').strip(),
                        status = "pending" if data.get('role').strip() == "manager" else "active")
        db.session.add(new_user)
        db.session.commit()
        
        return {"message" : "User signup successfully."}, 201 # successfully created
    