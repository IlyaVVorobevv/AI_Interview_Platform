import pytest


@pytest.mark.asyncio
async def test_success_login(create_user_helper):
    await create_user_helper(email="user67@example.com",
                             username="string67",
                             password="12345678",
                             auth_role="register")

    response_login = await create_user_helper(email="user67@example.com",
                                        username="string67",
                                        password="12345678",
                                        auth_role="login")

    assert response_login.status_code == 200
    data = response_login.json()
    assert data["access_token"]
    assert data["token_type"]
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_wrong_password(create_user_helper):
    await create_user_helper(email="user67@example.com",
                             username="string67",
                             password="12345678",
                             auth_role="register")

    response_login = await create_user_helper(email="user67@example.com",
                                        username="string67",
                                        password="12345678999",
                                        auth_role="login")
    assert response_login.status_code == 401
    data = response_login.json()
    assert data["detail"] == "Invalid email or password"

@pytest.mark.asyncio
async def test_login_unknown_user(create_user_helper):
    response_login = await create_user_helper(email="unknown@example.com",
                                        username="string67",
                                        password="12345678999",
                                        auth_role="login")
    assert response_login.status_code == 401
    data = response_login.json()
    assert data["detail"] == "Invalid email or password"
