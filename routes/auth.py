from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    
    if not name or not email or not password:
        return jsonify({"message": "Lütfen isim, email ve şifre alanlarını doldurun."}), 400

    # Email kayıtlı mı kontrol edelim
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Bu email zaten kayıtlı."}), 400

    # Yeni kullanıcı oluştur ve şifreyi hash'leyelim
    new_user = User(name=name, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    # Kullanıcı ID'sini identity olarak kullanarak JWT token oluşturma (1 gün geçerli)
    access_token = create_access_token(identity=new_user.id, expires_delta=datetime.timedelta(days=1))
    return jsonify({"token": access_token, "message": "Kayıt başarılı."}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Lütfen email ve şifre alanlarını doldurun."}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Geçersiz kimlik bilgileri."}), 401

    access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(days=1))
    return jsonify({"token": access_token, "message": "Giriş başarılı."}), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "Kullanıcı bulunamadı."}), 404

    user_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "weight": user.weight,
        "height": user.height,
        "gender": user.gender,
        "diet_goal": user.diet_goal,
        "allergies": user.allergies
    }
    return jsonify(user_data), 200

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "Kullanıcı bulunamadı."}), 404

    data = request.get_json()
    # İstenilen alanları güncelle
    user.name = data.get("name", user.name)
    user.age = data.get("age", user.age)
    user.weight = data.get("weight", user.weight)
    user.height = data.get("height", user.height)
    user.gender = data.get("gender", user.gender)
    user.diet_goal = data.get("diet_goal", user.diet_goal)
    user.allergies = data.get("allergies", user.allergies)

    db.session.commit()
    return jsonify({"message": "Profil güncellendi."}), 200
