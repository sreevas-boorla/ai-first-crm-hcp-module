"""LangGraph agent graph — the core AI agent for the CRM HCP module.

Architecture:
  User Message → LLM (Groq gemma2-9b-it) → Tool Decision → Execute Tools → LLM Response
  Uses a ReAct-style agent loop powered by LangGraph's StateGraph.
"""
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition

from agent.state import AgentState
from agent.tools import ALL_TOOLS

load_dotenv()

# ─── System prompt for the CRM agent ────────────────────────────────────
SYSTEM_PROMPT = """You are an AI assistant for a pharmaceutical CRM system, helping field sales representatives manage their interactions with Healthcare Professionals (HCPs).

Your capabilities:
1. **Log Interaction**: Record new meetings, calls, and engagements with HCPs. Extract structured data from natural language descriptions — interaction type, products discussed, key topics, HCP feedback, sentiment, and follow-up actions.
2. **Edit Interaction**: Modify previously logged interactions when the user wants to update or correct details.
3. **Search HCP**: Find doctors by name, specialty, or institution.
4. **Get Interaction History**: Retrieve past interaction records for a specific HCP.
5. **Suggest Follow-Up**: Recommend next-best actions based on interaction history and sentiment trends.
6. **Get Product Info**: Look up pharmaceutical products in the portfolio.

Guidelines:
- When the user describes a meeting or interaction in natural language, extract ALL relevant structured fields and use the log_interaction tool.
- Generate a concise ai_summary from the user's description.
- Infer sentiment (Positive/Neutral/Negative) from the description context.
- If the user doesn't specify an HCP, ask them to identify the doctor or search by name.
- Always confirm successful actions with a clear summary.
- Be professional, concise, and helpful — as expected in a pharmaceutical sales context.
- When extracting products, match them against known products if possible.
- **CRITICAL**: Before calling `edit_interaction`, you MUST know the exact integer `interaction_id`. If you do not have it or if the user asks to edit "the last interaction", you MUST first call `get_interaction_history` to fetch the recent interactions and identify the correct `interaction_id`. Never guess or pass placeholders/strings for `interaction_id`.
"""


def _build_graph():
    """Build and compile the LangGraph agent."""
    llm = ChatGroq(
        model=os.getenv("GROQ_MODEL", "gemma2-9b-it"),
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3,
        max_tokens=2048,
    )

    # Bind tools to the LLM
    llm_with_tools = llm.bind_tools(ALL_TOOLS)

    # ─── Node: Call the LLM ──────────────────────────────────────────
    def agent_node(state: AgentState):
        messages = state["messages"]
        # Prepend system prompt if not already present
        if not any(isinstance(m, SystemMessage) for m in messages):
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    # ─── Build the graph ─────────────────────────────────────────────
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode(ALL_TOOLS))

    # Set entry point
    graph.set_entry_point("agent")

    # Conditional edge: if the LLM called tools, execute them; otherwise end
    graph.add_conditional_edges("agent", tools_condition)

    # After tools execute, go back to agent for the final response
    graph.add_edge("tools", "agent")

    return graph.compile()


# ─── Singleton compiled graph ────────────────────────────────────────────
_compiled_graph = None


def get_agent():
    """Return the compiled LangGraph agent (singleton)."""
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = _build_graph()
    return _compiled_graph


async def run_agent(message: str, hcp_id: int = None):
    """Run the agent with a user message and optional HCP context.

    Returns the agent's final text reply plus any structured data.
    """
    agent = get_agent()

    # Build context-aware prompt
    user_msg = message
    if hcp_id:
        user_msg = f"[Context: The user is currently viewing HCP ID {hcp_id}]\n\n{message}"

    initial_state = {
        "messages": [HumanMessage(content=user_msg)],
        "hcp_id": hcp_id,
        "interaction_data": None,
        "action_taken": None,
    }

    # Run the graph
    result = await agent.ainvoke(initial_state)

    # Extract the final AI message
    final_messages = result.get("messages", [])
    ai_reply = ""
    for msg in reversed(final_messages):
        if hasattr(msg, "content") and msg.content and not hasattr(msg, "tool_calls"):
            ai_reply = msg.content
            break

    return {
        "reply": ai_reply or "I processed your request. Let me know if you need anything else.",
        "interaction_data": result.get("interaction_data"),
        "action_taken": result.get("action_taken"),
    }
