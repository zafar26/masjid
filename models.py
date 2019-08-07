from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Organisations(db.Model):
    __tablename__ = "organisations"
    id = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String, nullable=False)


class Members(db.Model):
    __tablename__ = "members"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    password = db.Column(db.Integer, nullable=False)

class Members_belongs_to(db.Model):
    __tablename__ = "members_belongs_to"
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey("organisations.id"),nullable=False)
    members_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    org_id = db.Column(db.Integer, db.ForeignKey("organisations.id"), nullable=False)

class Transaction(db.Model):
    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key=True)
    payee = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    income = db.Column(db.Integer, nullable=False)
    expense = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    org_id = db.Column(db.Integer, db.ForeignKey("organisations.id"), nullable=False)    
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)    
