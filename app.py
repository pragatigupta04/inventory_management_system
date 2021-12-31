from flask import Flask, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import traceback


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(150), unique=True, nullable=False)

class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_name = db.Column(db.String(150), unique=True, nullable=False)

class ProductMovement(db.Model):
    movement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    from_location = db.Column(db.String(150), db.ForeignKey("location.location_id"))
    to_location = db.Column(db.String(150), db.ForeignKey("location.location_id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"))
    product_qty = db.Column(db.Integer)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/add_product", methods=["POST", "GET"])
def add_product():
    print(request.method)
    if request.method == "POST":
        product_name = request.form.get('product_name')
        product = Product(product_name=product_name)
        db.session.add(product)
        db.session.commit()
        text = "Product Added Successfully!"
        return render_template("add_product.html", text=text)
    else:
        return render_template("add_product.html")

@app.route("/add_location", methods=["POST", "GET"])
def add_location():
    if request.method == "POST":
        location_name = request.form.get('location_name')
        location = Location(location_name=location_name)
        db.session.add(location)
        db.session.commit()
        text = "Location Added Successfully!"
        return render_template("add_location.html", text=text)
    else:
        return render_template("add_location.html")

@app.route("/add_product_movement", methods=["POST", "GET"])
def add_product_movement():
    if request.method == "POST":
        product_id = request.form.get('product_id')
        from_location = request.form.get('from_location')
        to_location = request.form.get('to_location')
        product_qty = request.form.get('product_qty')
        product = ProductMovement(product_id=product_id, from_location=from_location, to_location=to_location, product_qty=product_qty)
        db.session.add(product)
        db.session.commit()
        return render_template("add_product_movement.html")
    else:
        return render_template("add_product_movement.html")

@app.route("/view_products", methods=["GET"])
def view_products():
    products = Product.query.all()
    return render_template('view_products.html', products=products)

@app.route("/view_locations", methods=["GET"])
def view_locations():
    locations = Location.query.all()
    return render_template('view_locations.html', locations=locations)

@app.route("/view_product_movements", methods=["GET"])
def view_product_movements():
    product_movements = ProductMovement.query.all()
    return render_template('view_product_movements.html', product_movements=product_movements)

@app.route("/edit_product", methods=["POST", "GET"])
def edit_product():
    try:
        if request.method == "GET":
            productid = request.args.get('product_id')
            product_name = db.session.query(Product.product_name).filter(Product.product_id==productid).first()[0]
            return render_template('edit_product.html', product_id=productid, product_name=product_name)
        else:
            productid = request.form.get('product_id')
            product_name = request.form.get('product_name')
            print(productid, product_name)
            product = db.session.query(Product).filter(Product.product_id==productid).first()
            product.product_name = product_name
            db.session.flush()
            db.session.commit()
            return redirect('/')
    except Exception:
        print(traceback.format_exc())
        return "Error!"

@app.route("/edit_location", methods=["POST", "GET"])
def edit_location():
    try:
        if request.method == "GET":
            locationid = request.args.get('location_id')
            location_name = db.session.query(Location.location_name).filter(Location.location_id==locationid).first()[0]
            return render_template('edit_location.html', location_id=locationid, location_name=location_name)
        else:
            locationid = request.form.get('location_id')
            location_name = request.form.get('location_name')
            print(locationid, location_name)
            location = db.session.query(Location).filter(Location.location_id==locationid).first()
            location.location_name = location_name
            db.session.flush()
            db.session.commit()
            return redirect('/')
    except Exception:
        print(traceback.format_exc())
        return "Error!"

@app.route("/edit_product_movement", methods=["POST", "GET"])
def edit_product_movement():
    try:
        if request.method == "GET":
            movementid = request.args.get('movement_id')
            movement = db.session.query(ProductMovement).filter(ProductMovement.movement_id==movementid).first()
            product_id = movement.product_id
            from_location = movement.from_location
            to_location = movement.to_location
            product_qty = movement.product_qty
            timestamp = movement.timestamp
            return render_template('edit_product_movement.html', movement_id=movementid, product_id=product_id, from_location=from_location, to_location=to_location, product_qty=product_qty, timestamp=timestamp)
        else:
            movementid = request.form.get('movement_id')
            product_id = request.form.get('product_id')
            from_location = request.form.get('from_location')
            to_location = request.form.get('to_location')
            product_qty = request.form.get('product_qty')
            timestamp = request.form.get('timestamp')
            print(product_id, from_location)
            movement = db.session.query(ProductMovement).filter(ProductMovement.movement_id==movementid).first()
            movement.product_id = product_id
            movement.from_location = from_location
            movement.to_location = to_location
            movement.product_qty = product_qty
            db.session.flush()
            db.session.commit()
            return redirect('/')
    except Exception:
        print(traceback.format_exc())
        return "Error!"
    

if __name__ == "__main__":
    app.run(debug=True, port=8000)