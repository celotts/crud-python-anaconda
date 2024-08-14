import os
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../crud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

print("Database path:", os.path.abspath(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')))


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)


# Crear las tablas dentro del contexto de la aplicación
with app.app_context():
    db.create_all()


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Manejo de excepciones generales."""
    response = e.get_response()
    response.data = jsonify({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    }).data
    response.content_type = "application/json"
    return response


@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()

    # Validar parámetros de entrada
    if not data:
        abort(400, description="No data provided")
    if 'name' not in data:
        abort(400, description="Missing required parameters: 'name'")

        # Validar parámetros de entrada
    if 'description' not in data:
        abort(400, description="Missing required parameters: 'description'")

    new_item = Item(name=data['name'], description=data['description'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Item created successfully', 'id': new_item.id}), 201


@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    results = [
        {
            "id": item.id,
            "name": item.name,
            "description": item.description
        } for item in items]

    return jsonify(results), 200


@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    result = {
        "id": item.id,
        "name": item.name,
        "description": item.description
    }
    return jsonify(result), 200


@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()

    # Validar parámetros de entrada
    if not data:
        abort(400, description="No data provided")
    if 'name' not in data:
        abort(400, description="Missing required parameters: 'name'")

        # Validar parámetros de entrada
    if 'description' not in data:
        abort(400, description="Missing required parameters: 'description'")

    item = Item.query.get_or_404(item_id)
    item.name = data['name']
    item.description = data['description']
    db.session.commit()
    return jsonify({'message': 'Item updated successfully'}), 200


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5002)
