import pytest


@pytest.mark.asyncio
async def test_get_current_user(create_user_helper, client):
    await create_user_helper(email="user67@example.com",
                             username="string67",
                             password="12345678",
                             auth_role="register")

    response_login = await create_user_helper(email="user67@example.com",
                                              username="string67",
                                              password="12345678",
                                              auth_role="login")
    data = response_login.json()
    access_token = data["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response_user = await client.get("/users/me", headers=headers)

    assert response_user.status_code == 200

    data_user = response_user.json()

    assert data_user["email"] == "user67@example.com"
    assert data_user["username"] == "string67"
    assert data_user["id"] is not None


@pytest.mark.asyncio
async def test_get_current_user_without_token(create_user_helper, client):
    await create_user_helper(email="user67@example.com",
                             username="string67",
                             password="12345678",
                             auth_role="register")

    await create_user_helper(email="user67@example.com",
                                              username="string67",
                                              password="12345678",
                                              auth_role="login")

    response_user = await client.get("/users/me")

    assert response_user.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_with_invalid_token(create_user_helper, client):
    await create_user_helper(email="user67@example.com",
                             username="string67",
                             password="12345678",
                             auth_role="register")

    await create_user_helper(email="user67@example.com",
                                              username="string67",
                                              password="12345678",
                                              auth_role="login")
    headers = {
        "Authorization": f"Bearer Invalid"
    }

    response_user = await client.get("/users/me", headers=headers)

    assert response_user.status_code == 401
