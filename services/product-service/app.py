from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'products.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price}

@app.before_first_request
def init_db():
    db.create_all()

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    p = Product.query.get_or_404(product_id)
    return jsonify(p.to_dict())

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json() or {}
    name = data.get('name')
    price = data.get('price')
    if not name or price is None:
        return jsonify({"error": "name and price required"}), 400
    try:
        price = float(price)
    except ValueError:
        return jsonify({"error": "price must be a number"}), 400

    p = Product(name=name, price=price)
    db.session.add(p)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "could not create product"}), 500

    return jsonify(p.to_dict()), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
