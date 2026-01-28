from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt

from .models import db, Products, Category

class ProductApi(Resource):
    @jwt_required()
    def get(self):
        products = Products.query.all()   # list of category-alchemy-object
        
        product_json = []
        for product in products:
            product_json.append(product.convert_to_json())
        return product_json, 200

    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        current_user = get_jwt()
        if current_user.get("role") != "manager" :
            return {"message" : "Access Denied!!!"}, 403

        data = request.json
        if not (data.get("name") and data.get("description") and data.get("price") and data.get("unit")
                and data.get("stock") and data.get("category_id")):
            
            return {"message" : "Bad Request!! All fields are required."}, 400    
        


        product = Products.query.filter_by(name = data.get("name")).first()
        if product:
            return {"message" : f"{product.name} product already exists!"}, 400
        
        category = Category.query.get(data.get("category_id"))
        if not category:
            return {"message":"Category not found!"}, 404
        
        new_product = Products(name = data.get('name').strip(),description = data.get('description').strip(),
                               price = data.get('price'),unit = data.get('unit').strip(),
                               stock = data.get('stock'),sold_inventory = 0,
                               category_id = data.get('category_id'), manager_id = current_user_id)
        
        db.session.add(new_product)
        db.session.commit()
        
        return {"message" : "Product added successfully."}, 201 # successfully created

    @jwt_required()
    def put(self, product_id):
        current_user_id = get_jwt_identity()
        current_user = get_jwt()
        if current_user.get("role") != "manager" :
            return {"message" : "Access Denied!!!"}, 403
        
        # product = Products.query.get('product_id')
        product = Products.query.filter_by(id=product_id, manager_id = current_user_id)
        if not product:
            return {"message":"Product not found!"}, 404

        data = request.json
        
        product.name = data.get('name').strip() if data.get("name").strip() else product.name
        product.description = data.get('description').strip() if data.get("description").strip() else product.description
        product.price = data.get('price') if data.get("price") else product.price
        product.unit = data.get('unit').strip() if data.get("unit").strip() else product.unit
        product.stock = data.get('stock') if data.get("stock") else product.stock
       
        db.session.commit()
        
        return {"message" : "Product updated successfully."}, 200 # successfully updated

    @jwt_required()
    def delete(self, product_id):
        current_user_id = get_jwt_identity()
        current_user = get_jwt()
        if current_user.get("role") != "manager" :
            return {"message" : "Access Denied!!!"}, 403
        
        # product = Products.query.get('product_id')
        product = Products.query.filter_by(id=product_id, manager_id = current_user_id)
        if not product:
            return {"message":"Product not found!"}, 404
        
        db.session.delete(product)
        db.session.commit()
        
        return {"message" : "Product deleted successfully."}, 200 # successfully deleted

