from flask import Blueprint, request, jsonify
from app.services.chat_service import ChatService

upgrade_news_bp = Blueprint('upgrade_news', __name__, url_prefix='/api/upgrade_news')
chat_service = ChatService()

@upgrade_news_bp.route('/polish', methods=['POST'])
def polish_description():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No JSON data provided"}), 400

        raw_description = data.get('description')
        module = data.get('module')

        if not raw_description or not raw_description.strip():
            return jsonify({"status": "error", "message": "description is required"}), 400

        system_prompt = """You are a helpful assistant that converts technical descriptions into user-friendly announcements.

CRITICAL INSTRUCTION: Match the output language to the input language. If input is Traditional Chinese, output Traditional Chinese. If input is English, output English."""

        user_prompt = f"""Convert this technical description into a clear, professional announcement for end users. Remove technical jargon and make it concise and user-friendly:

{raw_description}"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        result = chat_service.process_with_messages('upgrade_news_polish', messages)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"status": "error", "message": "Internal server error"}), 500