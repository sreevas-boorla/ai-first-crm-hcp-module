"""CRUD operations for database models."""
from sqlalchemy.orm import Session
from models import HCP, Product, Interaction
from datetime import datetime


# ─── HCP CRUD ────────────────────────────────────────────────────────────
def get_hcps(db: Session, search: str = None):
    query = db.query(HCP)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (HCP.first_name.ilike(search_term))
            | (HCP.last_name.ilike(search_term))
            | (HCP.specialty.ilike(search_term))
            | (HCP.institution.ilike(search_term))
        )
    return query.order_by(HCP.last_name).all()


def get_hcp(db: Session, hcp_id: int):
    return db.query(HCP).filter(HCP.id == hcp_id).first()


def create_hcp(db: Session, data: dict):
    hcp = HCP(**data)
    db.add(hcp)
    db.commit()
    db.refresh(hcp)
    return hcp


# ─── Product CRUD ────────────────────────────────────────────────────────
def get_products(db: Session):
    return db.query(Product).all()


# ─── Interaction CRUD ────────────────────────────────────────────────────
def get_interactions(db: Session, hcp_id: int = None):
    query = db.query(Interaction)
    if hcp_id:
        query = query.filter(Interaction.hcp_id == hcp_id)
    return query.order_by(Interaction.interaction_date.desc()).all()


def get_interaction(db: Session, interaction_id: int):
    return db.query(Interaction).filter(Interaction.id == interaction_id).first()


def create_interaction(db: Session, data: dict):
    if not data.get("interaction_date"):
        data["interaction_date"] = datetime.utcnow()
    interaction = Interaction(**data)
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


def update_interaction(db: Session, interaction_id: int, data: dict):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        return None
    for key, value in data.items():
        if value is not None:
            setattr(interaction, key, value)
    interaction.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(interaction)
    return interaction


def delete_interaction(db: Session, interaction_id: int):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if interaction:
        db.delete(interaction)
        db.commit()
        return True
    return False
