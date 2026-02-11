import io

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select

from app.db.base import Base
from app.db.session import engine
from app.main import app
from app.models.entities import Call, CallStatus
from app.services.transcription import TranscriptionService


async def _reset_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.mark.asyncio
async def test_register_login_upload_flow() -> None:
    await _reset_db()

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
        assert payload['analysis']['scores']['buying_intent_score'] >= 4

        listed = await client.get('/api/v1/calls', headers={'Authorization': f'Bearer {token}'})
        assert listed.status_code == 200
        assert len(listed.json()) == 1


@pytest.mark.asyncio
async def test_health_and_readiness() -> None:
    await _reset_db()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as client:
        health = await client.get('/health')
        assert health.status_code == 200
        assert health.json() == {'status': 'ok'}

        ready = await client.get('/ready')
        assert ready.status_code == 200
        assert ready.json() == {'status': 'ready'}


@pytest.mark.asyncio
async def test_upload_failure_marks_call_failed(monkeypatch: pytest.MonkeyPatch) -> None:
    await _reset_db()

    async def _raise(_: str) -> str:
        raise RuntimeError('transcription down')

    monkeypatch.setattr(TranscriptionService, 'transcribe', _raise)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as client:
        register = await client.post(
            '/api/v1/auth/register',
            json={
                'organization_name': 'Beta Inc',
                'full_name': 'Admin User',
                'email': 'admin@beta.com',
                'password': 'Password123!',
            },
        )
        assert register.status_code == 201

        login = await client.post(
            '/api/v1/auth/login',
            json={'email': 'admin@beta.com', 'password': 'Password123!'},
        )
        token = login.json()['access_token']

        upload = await client.post(
            '/api/v1/calls/upload',
            headers={'Authorization': f'Bearer {token}'},
            files={'file': ('test.txt', io.BytesIO(b'hello'), 'text/plain')},
        )
        assert upload.status_code == 500

    async with engine.begin() as conn:
        result = await conn.execute(select(Call.status, Call.analysis))
        rows = result.all()
        assert len(rows) == 1
        assert rows[0][0] == CallStatus.FAILED
        assert rows[0][1] == {'error': 'Analysis failed'}


@pytest.mark.asyncio
async def test_call_crm_sync_and_template_settings() -> None:
    await _reset_db()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as client:
        await client.post(
            '/api/v1/auth/register',
            json={
                'organization_name': 'Gamma Inc',
                'full_name': 'Manager User',
                'email': 'manager@gamma.com',
                'password': 'Password123!',
            },
        )
        login = await client.post(
            '/api/v1/auth/login', json={'email': 'manager@gamma.com', 'password': 'Password123!'}
        )
        token = login.json()['access_token']

        upload = await client.post(
            '/api/v1/calls/upload',
            headers={'Authorization': f'Bearer {token}'},
            files={'file': ('demo.txt', io.BytesIO(b'budget timeline next week demo'), 'text/plain')},
        )
        call_id = upload.json()['id']

        sync = await client.post(
            f'/api/v1/calls/{call_id}/sync-crm', headers={'Authorization': f'Bearer {token}'}
        )
        assert sync.status_code == 200
        assert sync.json()['crm_sync']['status'] == 'synced'

        updated = await client.get(
            f'/api/v1/calls/{call_id}', headers={'Authorization': f'Bearer {token}'}
        )
        assert updated.status_code == 200
        assert (
            updated.json()['analysis']['structured_payload']['crm_sync']['status'] == 'synced'
        )

        save_templates = await client.put(
            '/api/v1/settings/templates',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'crm_field_mapping': {'prospect_email': 'Contact.Email'},
                'call_analysis_template': {'framework': 'BANT'},
            },
        )
        assert save_templates.status_code == 200

        read_templates = await client.get(
            '/api/v1/settings/templates', headers={'Authorization': f'Bearer {token}'}
        )
        assert read_templates.status_code == 200
        assert read_templates.json()['call_analysis_template']['framework'] == 'BANT'
