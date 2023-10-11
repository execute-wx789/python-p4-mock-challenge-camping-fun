from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    signups = db.relationship("Signup", backref="activity",cascade="all, delete")

    # Add relationship
    serialize_rules = ("-signups.activity",)
    
    # Add serialization rules
    
    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    signups = db.relationship("Signup", backref="camper")

    serialize_rules = ("-signups.camper",)

    # Add relationship
    
    # Add serialization rules
    
    # Add validation
    
    @validates("name")
    def validate_name(self,key,name):
        if not name or len(name) < 1:
            raise ValueError("Empty value provided")
        return name

    @validates("age")
    def validate_age(self,key,age):
        if not 8 <= age <= 18:
            raise ValueError("Age value provided isn't within allowed range")
        return age
    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)

    camper_id = db.Column(db.Integer,db.ForeignKey("campers.id"))
    activity_id = db.Column(db.Integer,db.ForeignKey("activities.id"))

    serialize_rules = ("-camper.signups","-activity.signups",)

    # Add relationships
    
    # Add serialization rules
    
    # Add validation

    @validates("time")
    def validate_time(self,key,time):
        if not 0 <= time <= 23:
            raise ValueError("time value provided isn't within allowed range")
        return time
    
    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need.
