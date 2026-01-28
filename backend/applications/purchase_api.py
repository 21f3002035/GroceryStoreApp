from flask import request, current_app as app
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt

from .models import *

class CategoryApi(Resource):
    @jwt_required()
    def get(self):
        categories = Category.query.all()   # list of category-alchemy-object
        print(categories)
        category_json = []
        for category in categories:
            # category_json.append({"id":category.id, "name" : category.name})
            category_json.append(category.convert_to_json())
        return category_json, 200

    @jwt_required()
    def post(self):
        current_user = get_jwt()
        if current_user.get("role") != "admin" :
            return {"message" : "Access Denied!!!"}, 403

        data = request.json
        if not data.get("name"):
            
            return {"message" : "Bad Request!! All fields are required."}, 400    
        
        if len(data.get("name").strip()) > 101 or len(data.get("name").strip()) < 4:
            return {"message" : "Length of name must between 4-100 char."}, 400


        category = Category.query.filter_by(name = data.get("name")).first()
        if category:
            return {"message": f"{category.name} category already exists!"}, 400
        
        new_category = Category(name = data.get('name'))
        db.session.add(new_category)
        db.session.commit()
        
        return {"message" : "Category created successfully."}, 201 # successfully created

    @jwt_required()
    def put(self, category_id):
        current_user = get_jwt()
        if current_user.get("role") != "admin" :
            return {"message" : "Access Denied!!!"}, 403

        data = request.json
        if not data.get("name"):
            
            return {"message" : "Bad Request!! All fields are required."}, 400    
        
        if len(data.get("name").strip()) > 101 or len(data.get("name").strip()) < 4:
            return {"message" : "Length of name must between 4-100 char."}, 400


        category = Category.query.get(category_id)
        if not category:
            return {"message":"Category not found!"}, 404
        
        category.name = data.get('name').strip()
        db.session.commit()
        
        return {"message" : "Category updated successfully."}, 200 # successfully updated

    @jwt_required()
    def delete(self, category_id):
        current_user = get_jwt()
        if current_user.get("role") != "admin" :
            return {"message" : "Access Denied!!!"}, 403

        category = Category.query.get(category_id)
        if not category:
            return {"message":"Category not found!"}, 404
        
        db.session.delete(category)
        db.session.commit()
        
        return {"message" : "Category deleted successfully."}, 200 # successfully deleted

