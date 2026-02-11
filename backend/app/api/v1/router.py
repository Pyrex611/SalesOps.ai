from fastapi import APIRouter

from app.api.v1 import auth, calls, orgs, users

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(orgs.router)
api_router.include_router(users.router)
api_router.include_router(calls.router)
