import os
import json
from flask import Flask,jsonify
from datetime import datetime
from flask import Flask, session, render_template, jsonify, request, redirect
#from flask_session import Session
from tempfile import mkdtemp
from models import *
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = os.getenv("SECRET_KEY")
db.init_app(app)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


#Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

ma = Marshmallow(app)

class OrganisationsSchema(ma.ModelSchema):
    class Meta:
       model = Organisations


class MembersSchema(ma.ModelSchema):
    class Meta:
       model = Members

class Members_belongs_toSchema(ma.ModelSchema):
    class Meta:
       model = Members_belongs_to

class CategorySchema(ma.ModelSchema):
    class Meta:
       model = Category

class TransactionSchema(ma.ModelSchema):
    class Meta:
       model = Transaction


@app.route('/')
def index():
    return redirect('/organisation')


@app.route('/organisation', method="POST")
def organisation_post():
    json_obj = json.loads(response.decode('utf-8'))
    
    for org_name in json_obj["organisation"]:
        organisation= Organisation(org_name=org_name)
        db.session.add(organisation)
    db.session.commit()
    return jsonify('succes')

@app.route('/organisation', method="GET")
def organisation_get():
    organ = Organisations.query.all()
    organisation_schema = OrganisationsSchema(many=True)
    output = organisation_schema.dump(organ).data
    return jsonify({'organisations' : output})

@app.route('/transactions',method =["POST"])
def transactions_post():
    json_obj = json.loads(response.decode('utf-8'))

    #insert data in database(json_obj["products"][0]["upc"])
    for payee, description, income, expense, timestamp, org_id, category_id  in json_obj["transactions"]:
        transaction = Transaction(payee=payee, description=description, income=income, expense=expense, timestamp=timestamp, org_id=org_id, category_id=category_id)
        db.session.add(transaction)
    db.session.commit()
    return jsonify('succes')


@app.route('/transactions',method =["GET"])
def transactions_get():
    transactions = Transaction.query.all()
    transaction_schema = TransactionSchema(many=True)
    output = transaction_schema.dump(transactions).data
    return jsonify({'transactions' : output})
    
 
@app.route('/members')
def members():
    members = Members.query.all()
    members_schema = MembersSchema(many=True)
    output = members_schema.dump(members).data
    return jsonify({'members' : output})
 
 
@app.route('/members_belongs_to', methods=["GET"])
def members_belongs_to():
    members_details = Members_belongs_to.query.all()
    members_schema = Members_belongs_toSchema(many=True)
    output = members_schema.dump(members_details).data
    return jsonify({'members_belongs_to' : output})
 
 
@app.route('/members_belongs_to', methods=["POST"])
def members_belongs_to_post():
    json_obj = json.loads(response.decode('utf-8'))

    #insert data in database(json_obj["products"][0]["upc"])
    for org_id, members_id  in json_obj["members_belongs _to"]:
        members = Members_belongs_to(org_id=org_id, members_id=members_id)
        db.session.add(members)
    db.session.commit()
    return jsonify('succes')


@app.route('/category')
def category():
    categories = Category.query.all()
    category_schema = CategorySchema(many=True)
    output = category_schema.dump(categories).data
    return jsonify({'category' : output})
 

if __name__ == '__main__':
    app.run(debug=True)