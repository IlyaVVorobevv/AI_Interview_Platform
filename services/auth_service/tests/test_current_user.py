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

@pytest.mark.asyncio
async def test_get_users(create_user_helper, client):
    await create_user_helper(
        email="user1@example.com",
        username="user1",
        password="12345678",
        auth_role="register"
    )
    await create_user_helper(
        email="user2@example.com",
        username="user2",
        password="12345678",
        auth_role="register"
    )
    await create_user_helper(
        email="user3@example.com",
        username="user3",
        password="12345678",
        auth_role="register"
    )
    await create_user_helper(
        email="user4@example.com",
        username="user4",
        password="12345678",
        auth_role="register"
    )
    await create_user_helper(
        email="user5@example.com",
        username="user5",
        password="12345678",
        auth_role="register"
    )

    response_users = await client.get("/users")

    assert response_users.status_code == 200
    data = response_users.json()
    assert isinstance(data, list)
    assert len(data) == 5
    assert data[0]["email"] == "user1@example.com"
    assert data[4]["username"] == "user5"
    assert "password" not in data[4]
    assert "hashed_password" not in data[4]

@pytest.mark.asyncio
async def test_get_users_pagination(create_user_helper, client):
    await create_user_helper(
        email="user1@example.com",
        username="user1",
        password="12345678",
        auth_role="register"
    )
    await create_user_helper(
        email="user2@example.com",
        username="user2",
        password="12345678",
        auth_role="register"
    )
    await create_user_helper(
        email="user3@example.com",
        username="user3",
        password="12345678",
        auth_role="register"
    )
    await create_user_helper(
        email="user4@example.com",
        username="user4",
        password="12345678",
        auth_role="register"
    )
    await create_user_helper(
        email="user5@example.com",
        username="user5",
        password="12345678",
        auth_role="register"
    )
    response_users_without_offset = await client.get("/users?limit=2&offset=0")
    assert response_users_without_offset.status_code == 200

    data_without_offset = response_users_without_offset.json()
    assert data_without_offset[0]["email"] == "user1@example.com"
    assert data_without_offset[1]["email"] == "user2@example.com"
    assert len(data_without_offset) == 2

    response_users_with_offset = await client.get("/users?limit=2&offset=2")
    assert response_users_with_offset.status_code == 200

    data_with_offset = response_users_with_offset.json()
    assert data_with_offset[0]["email"] == "user3@example.com"
    assert data_with_offset[1]["email"] == "user4@example.com"
    assert len(data_with_offset) == 2

@pytest.mark.asyncio
async def test_get_users_empty(create_user_helper, client):
    response_users = await client.get("/users")
    assert response_users.status_code == 200
    data = response_users.json()
    assert data == []