from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_healthz() -> None:
    await app.router.startup()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/healthz")
    await app.router.shutdown()
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_auth_and_call_flow() -> None:
    await app.router.startup()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        org_resp = await client.post(
            "/api/v1/organizations", json={"name": f"SalesOps Org {uuid4()}"}
        )
        assert org_resp.status_code == 200
        org_id = org_resp.json()["id"]

        email = f"rep-{uuid4().hex[:8]}@example.com"
        create_user_resp = await client.post(
            "/api/v1/users",
            json={
                "organization_id": org_id,
                "email": email,
                "full_name": "Rep One",
                "password": "StrongPass123",
                "role": "rep",
            },
        )
        assert create_user_resp.status_code == 200

        login_resp = await client.post(
            "/api/v1/auth/login", json={"email": email, "password": "StrongPass123"}
        )
        assert login_resp.status_code == 200
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        upload = await client.post(
            "/api/v1/calls/upload",
            files={"file": ("sample.mp3", b"12345", "audio/mpeg")},
            headers=headers,
        )
        assert upload.status_code == 200

        list_resp = await client.get("/api/v1/calls", headers=headers)
        assert list_resp.status_code == 200
        assert len(list_resp.json()) >= 1
    await app.router.shutdown()
