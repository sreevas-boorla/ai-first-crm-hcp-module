"""Interaction API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import InteractionCreate, InteractionUpdate, InteractionResponse
import crud

router = APIRouter(prefix="/api/interactions", tags=["Interactions"])


@router.get("/", response_model=list[InteractionResponse])
def list_interactions(hcp_id: int = None, db: Session = Depends(get_db)):
    """List interactions, optionally filtered by HCP."""
    return crud.get_interactions(db, hcp_id=hcp_id)


@router.get("/{interaction_id}", response_model=InteractionResponse)
def get_interaction(interaction_id: int, db: Session = Depends(get_db)):
    """Get a single interaction by ID."""
    interaction = crud.get_interaction(db, interaction_id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction


@router.post("/", response_model=InteractionResponse, status_code=201)
def create_interaction(data: InteractionCreate, db: Session = Depends(get_db)):
    """Create a new interaction via structured form."""
    # Verify HCP exists
    hcp = crud.get_hcp(db, data.hcp_id)
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")
    return crud.create_interaction(db, data.model_dump())


@router.put("/{interaction_id}", response_model=InteractionResponse)
def update_interaction(interaction_id: int, data: InteractionUpdate, db: Session = Depends(get_db)):
    """Update an existing interaction."""
    updated = crud.update_interaction(db, interaction_id, data.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return updated


@router.delete("/{interaction_id}")
def delete_interaction(interaction_id: int, db: Session = Depends(get_db)):
    """Delete an interaction."""
    if not crud.delete_interaction(db, interaction_id):
        raise HTTPException(status_code=404, detail="Interaction not found")
    return {"success": True, "message": "Interaction deleted"}
