"""LangGraph agent state definition."""
from typing import Annotated, TypedDict, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """State schema for the LangGraph CRM agent."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    hcp_id: int | None
    interaction_data: dict | None
    action_taken: str | None
