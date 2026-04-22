"""HCP API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import HCPCreate, HCPResponse
import crud

router = APIRouter(prefix="/api/hcps", tags=["HCPs"])


@router.get("/", response_model=list[HCPResponse])
def list_hcps(search: str = None, db: Session = Depends(get_db)):
    """List all HCPs, optionally filtered by search term."""
    return crud.get_hcps(db, search=search)


@router.get("/{hcp_id}", response_model=HCPResponse)
def get_hcp(hcp_id: int, db: Session = Depends(get_db)):
    """Get a single HCP by ID."""
    hcp = crud.get_hcp(db, hcp_id)
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")
    return hcp


@router.post("/", response_model=HCPResponse, status_code=201)
def create_hcp(data: HCPCreate, db: Session = Depends(get_db)):
    """Create a new HCP."""
    return crud.create_hcp(db, data.model_dump())
