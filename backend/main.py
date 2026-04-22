"""FastAPI main application — AI-First CRM HCP Module."""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from database import engine, Base
from routers import hcps, interactions, agent_chat
from seed import seed

load_dotenv()

# Create tables
Base.metadata.create_all(bind=engine)

# Seed data on startup
seed()

app = FastAPI(
    title="AI-First CRM — HCP Module",
    description="A CRM system for pharmaceutical field representatives, powered by LangGraph and Groq LLM.",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:5173"), "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(hcps.router)
app.include_router(interactions.router)
app.include_router(agent_chat.router)


@app.get("/")
def root():
    return {
        "app": "AI-First CRM — HCP Module",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "hcps": "/api/hcps",
            "interactions": "/api/interactions",
            "agent_chat": "/api/agent/chat",
        },
    }


@app.get("/api/health")
def health():
    return {"status": "healthy", "service": "CRM HCP Module"}


@app.get("/api/products")
def list_products():
    from database import SessionLocal
    from models import Product
    db = SessionLocal()
    products = db.query(Product).all()
    db.close()
    return [{"id": p.id, "name": p.name, "therapeutic_area": p.therapeutic_area, "description": p.description} for p in products]
