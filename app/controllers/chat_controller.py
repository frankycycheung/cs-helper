from flask import Blueprint, request, jsonify
from app.services.chat_service import ChatService

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')
chat_service = ChatService()

@chat_bp.route('/', methods=['POST'])
def chat():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"status": "error", "message": "No JSON data provided"}), 400

        user_id = data.get('user_id')
        message = data.get('message')

        if not user_id:
            return jsonify({"status": "error", "message": "user_id is required"}), 400

        if not message or not message.strip():
            return jsonify({"status": "error", "message": "message cannot be empty"}), 400

        result = chat_service.process_message(user_id, message)
        return jsonify(result), 200

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": "Internal server error"}), 500