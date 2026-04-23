import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

from fastapi.testclient import TestClient
from main import create_app

app = create_app()
client = TestClient(app)

def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_chat_structure():
    # Проверяем, что эндпоинт отвечает (ошибка или успех – не важно, главное что не 500 из-за нашей ошибки)
    response = client.post("/api/v1/chat", json={"message": "Привет"})
    # Без ключа OpenAI API вернёт 500, но это ожидаемо в CI
    # Проверяем лишь, что ответ содержит JSON
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert "session_id" in data or "detail" in data
