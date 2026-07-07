from flask import Blueprint, request, jsonify, current_app
from src.database.db import db, bcrypt
from src.models.user_model import User
import jwt
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json or {}
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    if not name or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400
        
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400
        
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    new_user = User(name=name, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if user and bcrypt.check_password_hash(user.password_hash, password):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=7)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": user.to_dict()
        })
        
    return jsonify({"error": "Invalid email or password"}), 401
