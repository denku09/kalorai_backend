from flask import Blueprint, request, jsonify
from app import db
from app.models import Meal
from flask_jwt_extended import jwt_required, get_jwt_identity

meals_bp = Blueprint('meals', __name__)

@meals_bp.route('', methods=['POST'])
@jwt_required()
def add_meal():
    current_user = get_jwt_identity()
    data = request.get_json()
    food_name = data.get("food_name")
    portion = data.get("portion")
    calories = data.get("calories")
    
    if not food_name or portion is None or calories is None:
        return jsonify({"message": "Lütfen yiyecek adı, porsiyon ve kalori bilgilerini giriniz."}), 400
    
    new_meal = Meal(user_id=current_user, food_name=food_name, portion=portion, calories=calories)
    db.session.add(new_meal)
    db.session.commit()
    
    return jsonify({"message": "Yemek eklendi."}), 201

@meals_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    meals = Meal.query.filter_by(user_id=current_user).all()
    total_calories = sum(meal.calories for meal in meals)
    
    meals_data = []
    for meal in meals:
        meals_data.append({
            "id": meal.id,
            "food_name": meal.food_name,
            "portion": meal.portion,
            "calories": meal.calories,
            "timestamp": meal.timestamp.isoformat()
        })
        
    return jsonify({
        "total_calories": total_calories,
        "meals": meals_data
    }), 200
