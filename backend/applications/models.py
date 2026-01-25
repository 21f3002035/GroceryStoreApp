from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

#User Table, Category Table, Product table, Cart Table,
# Order table, CategoryRequest Table, 
# User : Customer Table, Manager Table, Admin Table 

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)
    role = db.Column(db.String, nullable = False, default = "customer") # customer, manager, admin
    status = db.Column(db.String, nullable = False, default = "active") # active, pending

    all_carts = db.relationship("Cart", backref = "users", cascade = "all, delete-orphan", lazy = True)
    category_request = db.relationship("CategoryRequest", backref = "users", lazy = True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False, unique = True)

    all_products = db.relationship("Products", backref = "belong_to", cascade = "all, delete-orphan", lazy = True)

class Products(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    price = db.Column(db.Integer, nullable = False)
    unit = db.Column(db.String, nullable = False)
    stock = db.Column(db.Integer, nullable = False)
    sold_inventory = db.Column(db.Integer, nullable = False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable = False)
    all_carts = db.relationship("Cart", backref = "products", cascade = "all, delete-orphan", lazy = True)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    quantity = db.Column(db.Integer, nullable = False)

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable = False)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    quantity = db.Column(db.Integer, nullable = False)
    date_of_purchase = db.Column(db.String, default = datetime.now(), nullable = False) 

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable = False)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    
class CategoryRequest(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False, unique = True)    
    category_id = db.Column(db.Integer, nullable = True)
    action = db.Column(db.String, nullable = False)     # CREATE, UPDATE, DELETE

    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    
    