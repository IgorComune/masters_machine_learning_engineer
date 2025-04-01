from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Configs  # Import the Configs class
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity)


app = Flask(__name__)
app.config.from_object(Configs)  # Use the Configs class
app.config['JWT_VERIFY_SUB'] = False
db = SQLAlchemy(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    time_minutes = db.Column(db.Integer, nullable=False)

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Usuário já existe'}), 400
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuário registrado com sucesso'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Credenciais inválidas'}), 401

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify({'msg': f'Usuário com ID {current_user_id} acessou a rota protegida.'}), 200




if __name__ == "__main__":
    app.run(debug=True)