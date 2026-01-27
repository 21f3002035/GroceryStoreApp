from flask import request, current_app as app
from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt

from .models import *


class WelcomeApi(Resource):
    @jwt_required()
    def get(self):
        print("user_id :",get_jwt_identity())
        print("role :",get_jwt().get('role'))
        return {"message" : "Hello, this GroceryStore!"}, 200
    
    def post(self):
        data = request.json     # == request.get_json()
        print(request)
        print(data)
        msg = f'Hello! {data.get("name")}'
        return {'message' : msg}, 200