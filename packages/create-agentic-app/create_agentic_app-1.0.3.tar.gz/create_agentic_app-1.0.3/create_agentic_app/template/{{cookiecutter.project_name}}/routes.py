from fastapi import APIRouter

from agent_module.api import agent_router
from api_module.api import api_router

router = APIRouter()

router.include_router(
    api_router,
    prefix=""
)

router.include_router(
    agent_router,
    prefix="/chat"
)