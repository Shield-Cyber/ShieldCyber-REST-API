from . import CLIENT

def test_get_api_version_unauth():
    response = CLIENT.get("/version/get/api/version")
    assert response.status_code == 401