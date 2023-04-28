from . import CLIENT

def test_post_authenticate():
    content = {"username":"admin","password":"admin"}
    response = CLIENT.post("/authenticate", data=content)
    assert response.text
    assert response.status_code == 200