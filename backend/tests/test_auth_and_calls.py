import io

import pytest
from httpx import ASGITransport, AsyncClient

from app.db.base import Base
from app.db.session import engine
from app.main import app


@pytest.mark.asyncio
async def test_register_login_upload_flow() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as client:
        register = await client.post(
            '/api/v1/auth/register',
            json={
                'organization_name': 'Acme Inc',
                'full_name': 'Admin User',
                'email': 'admin@acme.com',
                'password': 'Password123!',
            },
        )
        assert register.status_code == 201

        login = await client.post(
            '/api/v1/auth/login',
            json={'email': 'admin@acme.com', 'password': 'Password123!'},
        )
        assert login.status_code == 200
        token = login.json()['access_token']

        upload = await client.post(
            '/api/v1/calls/upload',
            headers={'Authorization': f'Bearer {token}'},
            files={
                'file': (
                    'discovery.txt',
                    io.BytesIO(
                        b'Prospect discussed budget and timeline. I will send proposal next week.'
                    ),
                    'text/plain',
                )
            },
        )
        assert upload.status_code == 200
        payload = upload.json()
        assert payload['status'] == 'analyzed'
        assert payload['analysis']['buying_intent_score'] >= 4

        listed = await client.get('/api/v1/calls', headers={'Authorization': f'Bearer {token}'})
        assert listed.status_code == 200
        assert len(listed.json()) == 1
