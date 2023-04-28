from . import CLIENT

def test_get_ping():
    response = CLIENT.get("/ping")
    assert response.text == "<response>pong</response>"
    assert response.status_code == 200