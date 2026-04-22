"""LangGraph tools for the CRM HCP agent. Minimum 5 tools as required."""
import json
from datetime import datetime
from langchain_core.tools import tool
from database import SessionLocal
from models import HCP, Interaction, Product


def _get_db():
    """Get a fresh DB session for tool execution."""
    return SessionLocal()


# ═══════════════════════════════════════════════════════════════════════════
# TOOL 1: LOG INTERACTION (Required)
# ═══════════════════════════════════════════════════════════════════════════
@tool
def log_interaction(
    hcp_id: int,
    interaction_type: str = "Detail Aid",
    duration_minutes: int = 15,
    products_discussed: str = "",
    key_topics: str = "",
    hcp_feedback: str = "",
    sentiment: str = "Neutral",
    follow_up_actions: str = "",
    raw_notes: str = "",
    ai_summary: str = "",
) -> str:
    """Log a new interaction with a Healthcare Professional (HCP).

    Use this tool to record details of a meeting, call, or engagement with an HCP.
    The tool captures interaction type, products discussed, key topics, HCP feedback,
    sentiment analysis, and follow-up actions.

    Args:
        hcp_id: The database ID of the HCP.
        interaction_type: Type of interaction (Detail Aid, Sample Drop, Speaker Program,
            Lunch and Learn, Virtual Meeting, Phone Call, Email, Conference, Other).
        duration_minutes: Duration of the interaction in minutes.
        products_discussed: Comma-separated list of product names discussed.
        key_topics: Key topics covered during the interaction.
        hcp_feedback: Feedback or concerns raised by the HCP.
        sentiment: Overall sentiment (Positive, Neutral, Negative).
        follow_up_actions: Planned follow-up actions.
        raw_notes: Raw notes from the field representative.
        ai_summary: AI-generated summary of the interaction.
    """
    db = _get_db()
    try:
        hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
        if not hcp:
            return json.dumps({"error": f"HCP with ID {hcp_id} not found."})

        interaction = Interaction(
            hcp_id=hcp_id,
            interaction_type=interaction_type,
            interaction_date=datetime.utcnow(),
            duration_minutes=duration_minutes,
            products_discussed=products_discussed,
            key_topics=key_topics,
            hcp_feedback=hcp_feedback,
            sentiment=sentiment,
            follow_up_actions=follow_up_actions,
            raw_notes=raw_notes,
            ai_summary=ai_summary,
        )
        db.add(interaction)
        db.commit()
        db.refresh(interaction)

        return json.dumps({
            "success": True,
            "message": f"Interaction #{interaction.id} logged successfully for Dr. {hcp.first_name} {hcp.last_name}.",
            "interaction_id": interaction.id,
            "hcp_name": f"Dr. {hcp.first_name} {hcp.last_name}",
        })
    finally:
        db.close()


# ═══════════════════════════════════════════════════════════════════════════
# TOOL 2: EDIT INTERACTION (Required)
# ═══════════════════════════════════════════════════════════════════════════
@tool
def edit_interaction(
    interaction_id: int,
    interaction_type: str = None,
    duration_minutes: int = None,
    products_discussed: str = None,
    key_topics: str = None,
    hcp_feedback: str = None,
    sentiment: str = None,
    follow_up_actions: str = None,
    raw_notes: str = None,
) -> str:
    """Edit an existing logged interaction with an HCP.

    Use this tool to modify details of a previously logged interaction. Only provided
    fields will be updated; omitted fields remain unchanged.

    Args:
        interaction_id: The database ID of the interaction to edit.
        interaction_type: Updated type of interaction.
        duration_minutes: Updated duration in minutes.
        products_discussed: Updated comma-separated list of products.
        key_topics: Updated key topics.
        hcp_feedback: Updated HCP feedback.
        sentiment: Updated sentiment (Positive, Neutral, Negative).
        follow_up_actions: Updated follow-up actions.
        raw_notes: Updated raw notes.
    """
    db = _get_db()
    try:
        interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
        if not interaction:
            return json.dumps({"error": f"Interaction #{interaction_id} not found."})

        updates = {}
        if interaction_type is not None:
            interaction.interaction_type = interaction_type
            updates["interaction_type"] = interaction_type
        if duration_minutes is not None:
            interaction.duration_minutes = duration_minutes
            updates["duration_minutes"] = duration_minutes
        if products_discussed is not None:
            interaction.products_discussed = products_discussed
            updates["products_discussed"] = products_discussed
        if key_topics is not None:
            interaction.key_topics = key_topics
            updates["key_topics"] = key_topics
        if hcp_feedback is not None:
            interaction.hcp_feedback = hcp_feedback
            updates["hcp_feedback"] = hcp_feedback
        if sentiment is not None:
            interaction.sentiment = sentiment
            updates["sentiment"] = sentiment
        if follow_up_actions is not None:
            interaction.follow_up_actions = follow_up_actions
            updates["follow_up_actions"] = follow_up_actions
        if raw_notes is not None:
            interaction.raw_notes = raw_notes
            updates["raw_notes"] = raw_notes

        interaction.updated_at = datetime.utcnow()
        db.commit()

        return json.dumps({
            "success": True,
            "message": f"Interaction #{interaction_id} updated successfully.",
            "updated_fields": updates,
        })
    finally:
        db.close()


# ═══════════════════════════════════════════════════════════════════════════
# TOOL 3: SEARCH HCP
# ═══════════════════════════════════════════════════════════════════════════
@tool
def search_hcp(query: str) -> str:
    """Search for Healthcare Professionals by name, specialty, or institution.

    Use this tool when the user mentions a doctor's name, specialty, or institution
    and you need to find matching HCPs in the system.

    Args:
        query: Search term — can be a name, specialty (e.g., Cardiology), or institution.
    """
    db = _get_db()
    try:
        search_term = f"%{query}%"
        results = (
            db.query(HCP)
            .filter(
                (HCP.first_name.ilike(search_term))
                | (HCP.last_name.ilike(search_term))
                | (HCP.specialty.ilike(search_term))
                | (HCP.institution.ilike(search_term))
            )
            .limit(10)
            .all()
        )

        if not results:
            return json.dumps({"results": [], "message": f"No HCPs found matching '{query}'."})

        hcps = [
            {
                "id": h.id,
                "name": f"Dr. {h.first_name} {h.last_name}",
                "specialty": h.specialty,
                "institution": h.institution,
                "city": h.city,
                "tier": h.tier,
            }
            for h in results
        ]
        return json.dumps({"results": hcps, "count": len(hcps)})
    finally:
        db.close()


# ═══════════════════════════════════════════════════════════════════════════
# TOOL 4: GET INTERACTION HISTORY
# ═══════════════════════════════════════════════════════════════════════════
@tool
def get_interaction_history(hcp_id: int, limit: int = 5) -> str:
    """Retrieve the recent interaction history for a specific HCP.

    Use this tool to look up past engagements with a doctor before or after a meeting.
    This helps field reps prepare and maintain continuity.

    Args:
        hcp_id: The database ID of the HCP.
        limit: Maximum number of recent interactions to return (default 5).
    """
    db = _get_db()
    try:
        hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
        if not hcp:
            return json.dumps({"error": f"HCP with ID {hcp_id} not found."})

        interactions = (
            db.query(Interaction)
            .filter(Interaction.hcp_id == hcp_id)
            .order_by(Interaction.interaction_date.desc())
            .limit(limit)
            .all()
        )

        history = [
            {
                "id": i.id,
                "date": i.interaction_date.isoformat() if i.interaction_date else "",
                "type": i.interaction_type,
                "duration_minutes": i.duration_minutes,
                "products": i.products_discussed,
                "topics": i.key_topics,
                "sentiment": i.sentiment,
                "summary": i.ai_summary or i.raw_notes[:200] if i.raw_notes else "",
                "follow_up": i.follow_up_actions,
            }
            for i in interactions
        ]
        return json.dumps({
            "hcp": f"Dr. {hcp.first_name} {hcp.last_name}",
            "specialty": hcp.specialty,
            "total_interactions": len(history),
            "history": history,
        })
    finally:
        db.close()


# ═══════════════════════════════════════════════════════════════════════════
# TOOL 5: SUGGEST FOLLOW-UP ACTIONS
# ═══════════════════════════════════════════════════════════════════════════
@tool
def suggest_follow_up(hcp_id: int) -> str:
    """Suggest next-best follow-up actions for an HCP based on their interaction history.

    Use this tool to generate AI-powered recommendations for what a field rep should
    do next with a specific doctor, based on past engagements, sentiment trends, and
    products discussed.

    Args:
        hcp_id: The database ID of the HCP.
    """
    db = _get_db()
    try:
        hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
        if not hcp:
            return json.dumps({"error": f"HCP with ID {hcp_id} not found."})

        interactions = (
            db.query(Interaction)
            .filter(Interaction.hcp_id == hcp_id)
            .order_by(Interaction.interaction_date.desc())
            .limit(5)
            .all()
        )

        sentiments = [i.sentiment for i in interactions]
        products = set()
        for i in interactions:
            if i.products_discussed:
                for p in i.products_discussed.split(","):
                    products.add(p.strip())

        last_interaction_date = interactions[0].interaction_date.isoformat() if interactions else "Never"

        return json.dumps({
            "hcp": f"Dr. {hcp.first_name} {hcp.last_name}",
            "specialty": hcp.specialty,
            "tier": hcp.tier,
            "total_logged_interactions": len(interactions),
            "last_interaction": last_interaction_date,
            "recent_sentiments": sentiments,
            "products_discussed_historically": list(products),
            "context": f"Based on {len(interactions)} interactions. The most recent sentiment was "
                       f"{'positive' if sentiments and sentiments[0] == 'Positive' else 'neutral or negative'}. "
                       f"Products discussed include: {', '.join(products) if products else 'none yet'}.",
        })
    finally:
        db.close()


# ═══════════════════════════════════════════════════════════════════════════
# TOOL 6: GET PRODUCT INFO
# ═══════════════════════════════════════════════════════════════════════════
@tool
def get_product_info(product_name: str = "") -> str:
    """Get information about pharmaceutical products in the portfolio.

    Use this to look up products when the user mentions a drug name or therapeutic area,
    or to list all available products.

    Args:
        product_name: Name or partial name of a product. Leave empty to list all products.
    """
    db = _get_db()
    try:
        if product_name:
            products = db.query(Product).filter(Product.name.ilike(f"%{product_name}%")).all()
        else:
            products = db.query(Product).all()

        result = [
            {
                "id": p.id,
                "name": p.name,
                "therapeutic_area": p.therapeutic_area,
                "description": p.description,
            }
            for p in products
        ]
        return json.dumps({"products": result, "count": len(result)})
    finally:
        db.close()


# ─── Collect all tools ──────────────────────────────────────────────────
ALL_TOOLS = [
    log_interaction,
    edit_interaction,
    search_hcp,
    get_interaction_history,
    suggest_follow_up,
    get_product_info,
]
