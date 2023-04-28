from app.main import app
from fastapi.testclient import TestClient

CLIENT = TestClient(app)