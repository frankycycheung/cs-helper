from typing import Dict, Any
from .ollama_service import OllamaService

class ChatService:
    def __init__(self, ollama_service: OllamaService = None):
        self.ollama_service = ollama_service or OllamaService()

    def process_message(self, user_id: str, message: str) -> Dict[str, Any]:
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")

        ai_reply = self.ollama_service.chat([{"role": "user", "content": message}])

        self._log_chat(user_id, message, ai_reply)

        return {"status": "success", "reply": ai_reply}

    def _log_chat(self, user_id: str, user_message: str, ai_reply: str):
        pass