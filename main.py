from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import random
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(500), nullable=False)
    seats = db.Column(db.String(500), nullable=False)
    has_toilet = db.Column(db.Boolean, default=False)
    has_wifi = db.Column(db.Boolean, default=False)
    has_sockets = db.Column(db.Boolean, default=False)
    can_take_calls = db.Column(db.Boolean, default=False)
    coffee_price = db.Column(db.Double(500), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "map_url": self.map_url,
            "img_url": self.img_url,
            "location": self.location,
            "seats": self.seats,
            "has_toilet": self.has_toilet,
            "has_wifi": self.has_wifi,
            "has_sockets": self.has_sockets,
            "can_take_calls": self.can_take_calls,
            "coffee_price": self.coffee_price
        }

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET"])
def get_random_cafe():
    random_cafe = db.session.execute(db.select(Cafe).order_by(db.sql.func.random()).limit(1)).scalar()
    print(random_cafe)
    return jsonify(Cafe=random_cafe.to_dict())

@app.route("/all")
def get_all_cafes():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])

@app.route("/search")
def get_cafe_at_location():
    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    all_cafes = result.scalars().all()
    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location"})


@app.route("/add_cafe", methods=['POST'])
def add_cafe():
    name = request.args.get('name')
    map_url = request.args.get('map_url')
    img_url = request.args.get('img_url')
    location = request.args.get('location')
    seats = request.args.get('seats')
    has_toilet = request.args.get('has_toilet')
    has_wifi = request.args.get('has_wifi')
    has_sockets = request.args.get('has_sockets')
    can_take_calls = request.args.get('can_take_calls')
    coffee_price = request.args.get('coffee_price')

    new_cafe = Cafe(
        name=name,
        map_url=map_url,
        img_url=img_url,
        location=location,
        seats=seats,
        # has_toilet=has_toilet,
        # has_wifi=has_wifi,
        # has_sockets=has_sockets,
        # can_take_calls=can_take_calls,
        coffee_price=coffee_price
    )

    db.session.add(new_cafe)
    db.session.commit()

    return "Added"

@app.route("/update", methods=['PATCH'])
def update():
    id = request.args.get('id')
    parameter = request.args.get('parameter')
    value = request.args.get('value')
    cafe = Cafe.query.get(id)
    setattr(cafe, parameter, value)
    db.session.commit()
    return "Updated"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
