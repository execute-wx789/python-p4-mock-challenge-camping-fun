#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return ''

class Campers(Resource):
    def get(self):
        return_list = [c.to_dict(rules=("-signups",)) for c in Camper.query.all()]
        # return_list = []
        # for c in Camper.query.all():
        #     append_obj = {
        #         "name": c.name,
        #         "age": c.age,
        #         "id": c.id,
        #     }
        #     return_list.append(append_obj)
        return make_response(return_list,200)
    def post(self):
        form_json = request.get_json()
        try:
            new_camper = Camper(
                name=form_json["name"],
                age=int(form_json["age"]),
            )
        except ValueError:
            return make_response({"errors":"Error during camper formation"},400)
        db.session.add(new_camper)
        db.session.commit()

        camper_return = new_camper.to_dict()

        return make_response(camper_return,201)
api.add_resource(Campers,"/campers")

class CamperID(Resource):
    def get(self,id):
        c = Camper.query.filter_by(id=id).first()
        if not c:
            return make_response({"error":"Camper not found"},404)
        return make_response(c.to_dict(),200)
    def patch(self,id):
        c = Camper.query.filter_by(id=id).first()
        if not c:
            return make_response({"error":"Camper not found"},404)
        request_json = request.get_json()

        # setattr(c,"name",request_json["name"])
        # setattr(c,"age",int(request_json["age"]))

        for attr in request_json:
            try:
                setattr(c,attr,request_json[attr])
            except ValueError:
                return make_response({"errors":["validation errors"]},400)

        db.session.add(c)
        db.session.commit()

        camper_return = c.to_dict()
        return make_response(camper_return,202)
api.add_resource(CamperID,"/campers/<int:id>")

class Activities(Resource):
    def get(self):
        return_list = [a.to_dict(rules=("-signups",)) for a in Activity.query.all()]
        # return_list = []
        # for a in Activity.query.all():
        #     append_obj = {
        #         "name": a.name,
        #         "difficulty": a.difficulty,
        #         "id": a.id,
        #     }
        #     return_list.append(append_obj)
        return make_response(return_list,200)
api.add_resource(Activities,"/activities")
class ActivityID(Resource):
    def get(self,id):
        a = Activity.query.filter_by(id=id).first()
        if not a:
            return make_response({"error":"Activity not found"},404)
        return make_response(a.to_dict(),200)
    def delete(self,id):
        a = Activity.query.filter_by(id=id).first()
        if not a:
            return make_response({"error":"Activity not found"},404)
        db.session.delete(a)
        db.session.commit()

        return make_response("",204)
api.add_resource(ActivityID,"/activities/<int:id>")
class Signups(Resource):
    def get(self):
        return_list = []
        for s in Signup.query.all():
            append_obj = {
                "camper_id": s.camper_id,
                "activity_id": s.activity_id,
                "time": s.time,
                "id": s.id,
            }
            return_list.append(append_obj)
        return make_response(return_list,200)
    def post(self):
        form_json = request.get_json()
        try:
            new_signup = Signup(
                time=form_json["time"],
                camper_id=int(form_json["camper_id"]),
                activity_id=int(form_json["activity_id"]),
            )
        except ValueError as e:
            return make_response({"errors":["validation errors"]},400)
        db.session.add(new_signup)
        db.session.commit()

        signup_return = new_signup.to_dict()

        return make_response(signup_return,201)
api.add_resource(Signups,"/signups")

if __name__ == '__main__':
    app.run(port=5555, debug=True)-
