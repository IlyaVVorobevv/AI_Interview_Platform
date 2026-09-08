from sqlalchemy import select
from app.models.user import User

import pytest


@pytest.mark.asyncio
async def test_create_user(create_user_helper, get_user_helper):
    response = await create_user_helper(email="user67@example.com",
                                        username="string67",
                                        password="12345678")

    assert response.status_code == 201
    data = response.json()
    required_fields = {"id", "username", "email", "is_active", "created_at"}
    assert required_fields.issubset(data.keys())
    assert "password" not in data and "hashed_password" not in data

    db_user = await get_user_helper("user67@example.com")
    assert db_user is not None
    assert db_user.email == "user67@example.com"
    assert db_user.username == "string67"
    assert db_user.hashed_password != "12345678"

    assert data["id"] == db_user.id

@pytest.mark.asyncio
async def test_duplicate_email(create_user_helper, get_user_helper):
    first_response = await create_user_helper(email="test@example.com",
                                     username="user1",
                                     password="12345678")
    second_response = await create_user_helper(email="test@example.com",
                                     username="user2",
                                     password="12345678")

    assert first_response.status_code == 201
    assert second_response.status_code == 400

    second_data = second_response.json()
    assert second_data["detail"] == "Email already registered"

    db_first_user = await get_user_helper("test@example.com")
    assert db_first_user is not None


@pytest.mark.asyncio
async def test_duplicate_username(create_user_helper, get_user_helper):
    first_response = await create_user_helper(email="test1@example.com",
                                     username="user",
                                     password="12345678")
    second_response = await create_user_helper(email="test2@example.com",
                                     username="user",
                                     password="12345678")

    assert first_response.status_code == 201
    assert second_response.status_code == 400

    second_data = second_response.json()
    assert second_data["detail"] == "Username already registered"

    db_first_user = await get_user_helper("test1@example.com")
    assert db_first_user is not None



