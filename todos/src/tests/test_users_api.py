def test_user_sign_up(client):

    body = {
        "username": "test",
        "password": "plain_password"
    }
    response = client.post("/users/sign-up")
    assert response.status_code == 201
    assert response.json() is True