


async def test_create_user(client, db_session):
    response = await client.post("/auth/register", json={"email"   : "user67@example.com",
                                                   "username": "string67",
                                                   "password": "12345678"})
    user = db_session()
    assert response.status_code == 201
    data = response.json()
    required_fields = {"id", "username", "email", "is_active", "created_at"}
    assert required_fields.issubset(data.keys())
    assert "password" not in data




