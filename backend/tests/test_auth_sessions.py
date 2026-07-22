import pytest

PHONE_A = "+998901111111"
PHONE_B = "+998902222222"


async def _login(client, phone: str = PHONE_A, device_name: str | None = "test-device") -> dict:
    response = await client.post(
        "/api/v1/auth/otp/verify",
        json={"phone": phone, "code": "123456", "device_name": device_name},
    )
    assert response.status_code == 200
    return response.json()


def _auth_header(access_token: str) -> dict:
    return {"Authorization": f"Bearer {access_token}"}


@pytest.mark.asyncio
async def test_verify_otp_issues_access_and_refresh_tokens(client):
    tokens = await _login(client)
    assert tokens["access_token"]
    assert tokens["refresh_token"]
    assert tokens["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_verify_otp_rejects_wrong_code(client):
    response = await client.post(
        "/api/v1/auth/otp/verify", json={"phone": PHONE_A, "code": "000000"}
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_refresh_issues_new_access_token(client):
    tokens = await _login(client)
    response = await client.post(
        "/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]}
    )
    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["access_token"] != tokens["access_token"]


@pytest.mark.asyncio
async def test_refresh_rejects_unknown_token(client):
    response = await client.post(
        "/api/v1/auth/refresh", json={"refresh_token": "not-a-real-token"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout_revokes_session(client):
    tokens = await _login(client)

    logout_response = await client.post(
        "/api/v1/auth/logout", json={"refresh_token": tokens["refresh_token"]}
    )
    assert logout_response.status_code == 204

    refresh_response = await client.post(
        "/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]}
    )
    assert refresh_response.status_code == 401


@pytest.mark.asyncio
async def test_logout_is_idempotent(client):
    tokens = await _login(client)
    first = await client.post("/api/v1/auth/logout", json={"refresh_token": tokens["refresh_token"]})
    second = await client.post("/api/v1/auth/logout", json={"refresh_token": tokens["refresh_token"]})
    assert first.status_code == 204
    assert second.status_code == 204


@pytest.mark.asyncio
async def test_sessions_list_requires_authentication(client):
    response = await client.get("/api/v1/auth/sessions")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_sessions_list_shows_current_session(client):
    tokens = await _login(client)
    response = await client.get("/api/v1/auth/sessions", headers=_auth_header(tokens["access_token"]))
    assert response.status_code == 200
    sessions = response.json()
    assert len(sessions) == 1
    assert sessions[0]["is_current"] is True
    assert sessions[0]["device_name"] == "test-device"


@pytest.mark.asyncio
async def test_revoke_session_invalidates_its_refresh_token(client):
    tokens = await _login(client)
    sessions = (
        await client.get("/api/v1/auth/sessions", headers=_auth_header(tokens["access_token"]))
    ).json()
    session_id = sessions[0]["id"]

    revoke_response = await client.post(
        f"/api/v1/auth/sessions/{session_id}/revoke", headers=_auth_header(tokens["access_token"])
    )
    assert revoke_response.status_code == 204

    refresh_response = await client.post(
        "/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]}
    )
    assert refresh_response.status_code == 401


@pytest.mark.asyncio
async def test_revoke_session_is_scoped_to_owner(client):
    tokens_a = await _login(client, phone=PHONE_A)
    tokens_b = await _login(client, phone=PHONE_B)

    sessions_a = (
        await client.get("/api/v1/auth/sessions", headers=_auth_header(tokens_a["access_token"]))
    ).json()
    session_a_id = sessions_a[0]["id"]

    # User B must not be able to revoke user A's session.
    response = await client.post(
        f"/api/v1/auth/sessions/{session_a_id}/revoke", headers=_auth_header(tokens_b["access_token"])
    )
    assert response.status_code == 404

    # And user A's session must still be usable.
    refresh_response = await client.post(
        "/api/v1/auth/refresh", json={"refresh_token": tokens_a["refresh_token"]}
    )
    assert refresh_response.status_code == 200


@pytest.mark.asyncio
async def test_protected_endpoint_rejects_missing_auth(client):
    response = await client.get("/api/v1/cards")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_endpoint_accepts_valid_token(client):
    tokens = await _login(client)
    response = await client.get("/api/v1/cards", headers=_auth_header(tokens["access_token"]))
    assert response.status_code == 200
    assert response.json() == []
