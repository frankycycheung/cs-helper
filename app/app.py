from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.controllers.chat_controller import chat_bp
from app.controllers.upgrade_news_controller import upgrade_news_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.register_blueprint(chat_bp)
app.register_blueprint(upgrade_news_bp)

CORS(app)

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello from Flask!", "status": "success"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)