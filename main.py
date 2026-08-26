from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
import random

app = Flask(__name__)

class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("root.html")


@app.route("/suggestion")
def suggest_cafe():
    results = db.session.execute(db.Select(Cafe))
    cafes = results.scalars().all()
    random_cafe = random.choice(cafes)
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def show_all():
    results = db.session.execute(db.Select(Cafe))
    all_cafes = results.scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route("/wifi")
def has_wifi():
    results = db.session.execute(db.Select(Cafe).where(Cafe.has_wifi == True))
    wifi_cafes = results.scalars().all()
    return jsonify(wifi_cafes=[cafe.to_dict() for cafe in wifi_cafes])


@app.route("/add")
def add_cafe():
    new_cafe = Cafe(
        name=request.args.get("name"),
        map_url=request.args.get("map"),
        img_url=request.args.get("img"),
        location=request.args.get("loc"),
        seats=request.args.get("seats"),
        has_toilet=bool(request.args.get("toilet")),
        has_wifi=bool(request.args.get("wifi")),
        has_sockets=bool(request.args.get("sockets")),
        can_take_calls=bool(request.args.get("calls")),
        coffee_price=request.args.get("coffee_price")
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"Success": "New cafe successfully added!"})
#http://127.0.0.1:5000/add?name=hi&map=test&img=test&loc=here&seats=5&toilet=True&wifi=True&sockets=True&calls=True&coffee_price=$4

@app.route("/cafe/<name>")
def show_cafe(name):
    try:
        results = db.session.execute(db.Select(Cafe).where(Cafe.name == name))
        selected_cafe = results.scalars().one()
        return jsonify(cafe=selected_cafe.to_dict())
    except NoResultFound:
        return jsonify(error={"Error": "No cafe by that name in the database."}), 404

@app.route("/delete/<int:cafe_id>")
def remove_cafe(cafe_id):
    try:
        results = db.session.execute(db.Select(Cafe).where(Cafe.id == cafe_id))
        selected_cafe = results.scalars().one()
        db.session.delete(selected_cafe)
        db.session.commit()
        return jsonify(message={"Success": f"Cafe {selected_cafe.id} successfully removed."}), 200
    except NoResultFound:
        return jsonify(message={"Error": "No cafe by that name in the database."}), 404

@app.route("/update_price/<int:cafe_id>", methods=["GET","PATCH"])
def update_price(cafe_id):
    try:
        results = db.session.execute(db.Select(Cafe).where(Cafe.id == cafe_id))
        selected_cafe = results.scalars().one()
        selected_cafe.price = request.args.get("price")
        db.session.commit()
        return jsonify(message={
            "Success": f"Coffee price for {selected_cafe.name} successfully change to {selected_cafe.price}."}), 200
    except NoResultFound:
        return jsonify(message={"Error": "No cafe by that id in the database."}), 404

if __name__ == '__main__':
    app.run()