from flask import Blueprint, request, jsonify
import requests

analyze_bp = Blueprint('analyze', __name__)

@analyze_bp.route('', methods=['POST'])
def analyze_photo():
    data = request.get_json()
    image_data = data.get("image_data")
    if not image_data:
        return jsonify({"message": "Fotoğraf verisi eksik."}), 400
    
    # OpenAI API entegrasyonu (Endpoint ve API anahtarını uygun şekilde ayarlayın)
    openai_api_url = "https://api.openai.com/v1/your_endpoint"  # Gerçek uç noktayı girin
    headers = {
        "Authorization": "Bearer YOUR_OPENAI_API_KEY",  # Render'da environment variable olarak eklenebilir
        "Content-Type": "application/json"
    }
    payload = {
        "image": image_data
    }
    
    response = requests.post(openai_api_url, headers=headers, json=payload)
    if response.status_code != 200:
        return jsonify({"message": "Fotoğraf analizi başarısız."}), response.status_code

    result = response.json()
    estimated_calories = result.get("estimated_calories", 0)
    return jsonify({"estimated_calories": estimated_calories}), 200
