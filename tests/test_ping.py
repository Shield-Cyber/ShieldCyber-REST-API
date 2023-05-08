from . import CLIENT

def test_get_ping():
    response = CLIENT.get("/ping")
    assert response.text == '<ping_response status="200" status_text="pong"/>'
    assert response.status_code == 200