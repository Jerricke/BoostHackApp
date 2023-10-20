from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from config import db, bcrypt


# Models go here!
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    pfp = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("username")
    def validate_username(self, key, value):
        usernames = User.query.all()
        if not value and value in usernames:
            raise ValueError("Username already taken")
        return value

    @validates("dob")
    def validate_age(self, key, value):
        if not value:
            raise ValueError("Please provide DOB")
        return value

    @validates("email")
    def validate_email(self, key, value):
        if not value or "@" not in value:
            raise ValueError("Please provide valid email address")
        emails = User.query.all()
        if value in emails:
            raise ValueError("Email address already in use")
        return value

    @hybrid_property
    def password_hash(self):
        raise Exception("Password hashes may not be viewed")

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode("utf-8"))
        self._password_hash = password_hash.decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))


class Connection(db.Model):
    __tablename__ = "connections"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    pfp = db.Column(db.String)
    phone_number = db.Column(db.Integer)
    address = db.Column(db.String)
    notes = db.Column(db.String)
    classification = db.Column(db.String, nullable=False)
    favorite = db.Column(db.Boolean, default=False)
    dob = db.Column(db.DateTime)
    last_checked = db.Column(db.DateTime)
    first_contact_location = db.Column(db.String, nullable=False)
    first_contact_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("name")
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Please provide a name")
        return value

    @validates("classification")
    def validate_classification(self, key, value):
        classification_list = ["family", "professional", "friends", "undetermined"]
        if not value or value not in classification_list:
            raise ValueError("Please select a classification")
        return value

    @validates("first_contact_location")
    def validates_first_contact_location(self, key, value):
        if not value:
            raise ValueError("Please provide a first contact location")
        return value

    @validates("first_contact_date")
    def validates_first_contact_location(self, key, value):
        if not value:
            raise ValueError("Please provide a first contact date")
        return value
