from fastapi.testclient import TestClient
from main import app

client=TestClient(app)

def test_get_all_blogs():
    response= client.get("/blog/all")
    assert response.status_code == 200


def test_auth_error1():
    response = client.post("/token", data={"username": "", "password": ""})

    # Acceptable error status codes: 400 (bad input), 401 (unauth), 422 (validation)
    assert response.status_code in [400, 401, 422, 404]

    try:
        # If response is JSON, parse it
        data = response.json()

        if "detail" in data:
            # 422 or FastAPI-style error
            detail = data["detail"]
            if isinstance(detail, list):
                assert detail[0]["msg"] == "field required"
            else:
                assert "Invalid credentials" in detail
        else:
            # Generic check
            assert data.get("access_token") is None

    except Exception:
        # If not JSON, fallback to raw string check
        assert "Invalid credentials" in response.text or "Bad Request" in response.text


def test_auth_success():
    response = client.post("/token",data={"username":"aa","password":"123"})
    access_token=response.json().get("access_token")
    assert access_token

def test_post_article():
    auth=client.post("/token",data={"username":"aa","password":"123"})
    access_token=auth.json().get("access_token")
    assert access_token
    response=client.post("/article/",
                         json={"title":"Test article",
                               "content":"Test content",
                               "published": True,
                               "creator_id": 1
                               },
                        headers= {"Authorization": "bearer "+ access_token}
                         )
    assert response.status_code==200
    assert response.json().get("title")=="Test article"