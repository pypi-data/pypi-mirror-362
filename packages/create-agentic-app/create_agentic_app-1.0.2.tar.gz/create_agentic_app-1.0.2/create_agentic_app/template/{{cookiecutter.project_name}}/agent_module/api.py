from fastapi import APIRouter

from agent_module.agent import APISelectorAgent
from agent_module.model import Query

agent_router = APIRouter()
agent = APISelectorAgent()


@agent_router.post("/query")
async def get_query_response(query: Query):
    return await agent.process_query(query.query)
