"""AI Agent chat endpoint — conversational interface powered by LangGraph."""
import traceback
from fastapi import APIRouter, HTTPException
from schemas import ChatMessage, ChatResponse
from agent.graph import run_agent

router = APIRouter(prefix="/api/agent", tags=["AI Agent"])


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(msg: ChatMessage):
    """Send a message to the LangGraph CRM agent.

    The agent can:
    - Log interactions from natural language descriptions
    - Edit existing interactions
    - Search for HCPs
    - Retrieve interaction history
    - Suggest follow-up actions
    - Look up product information
    """
    try:
        result = await run_agent(message=msg.message, hcp_id=msg.hcp_id)
        return ChatResponse(
            reply=result["reply"],
            interaction_data=result.get("interaction_data"),
            action_taken=result.get("action_taken"),
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

