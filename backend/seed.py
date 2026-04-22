"""Seed script — populates the database with sample HCPs, products, and interactions."""
from database import SessionLocal, engine, Base
from models import HCP, Product, Interaction
from datetime import datetime, timedelta


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Skip if data exists
    if db.query(HCP).count() > 0:
        print("Database already seeded. Skipping.")
        db.close()
        return

    # ─── HCPs ────────────────────────────────────────────────────────
    hcps = [
        HCP(first_name="Sarah", last_name="Chen", specialty="Cardiology",
            institution="Mount Sinai Hospital", city="New York", state="NY",
            tier="A", email="s.chen@mountsinai.org", phone="212-555-0101"),
        HCP(first_name="James", last_name="Patel", specialty="Oncology",
            institution="Mayo Clinic", city="Rochester", state="MN",
            tier="A", email="j.patel@mayo.edu", phone="507-555-0202"),
        HCP(first_name="Maria", last_name="Rodriguez", specialty="Endocrinology",
            institution="Cleveland Clinic", city="Cleveland", state="OH",
            tier="B", email="m.rodriguez@ccf.org", phone="216-555-0303"),
        HCP(first_name="Robert", last_name="Kim", specialty="Neurology",
            institution="Johns Hopkins", city="Baltimore", state="MD",
            tier="A", email="r.kim@jhmi.edu", phone="410-555-0404"),
        HCP(first_name="Emily", last_name="Thompson", specialty="Pulmonology",
            institution="Mass General Hospital", city="Boston", state="MA",
            tier="B", email="e.thompson@mgh.harvard.edu", phone="617-555-0505"),
        HCP(first_name="David", last_name="Martinez", specialty="Rheumatology",
            institution="Stanford Medical Center", city="Palo Alto", state="CA",
            tier="B", email="d.martinez@stanford.edu", phone="650-555-0606"),
        HCP(first_name="Lisa", last_name="Wang", specialty="Cardiology",
            institution="UCSF Medical Center", city="San Francisco", state="CA",
            tier="A", email="l.wang@ucsf.edu", phone="415-555-0707"),
        HCP(first_name="Michael", last_name="Johnson", specialty="Dermatology",
            institution="Northwestern Memorial", city="Chicago", state="IL",
            tier="C", email="m.johnson@nm.org", phone="312-555-0808"),
    ]
    db.add_all(hcps)
    db.commit()

    # ─── Products ────────────────────────────────────────────────────
    products = [
        Product(name="CardioMax", therapeutic_area="Cardiovascular",
                description="Novel anticoagulant for atrial fibrillation. Once-daily dosing with superior bioavailability."),
        Product(name="OncoShield", therapeutic_area="Oncology",
                description="Immune checkpoint inhibitor targeting PD-L1 for advanced NSCLC and melanoma."),
        Product(name="NeuroCalm", therapeutic_area="Neurology",
                description="Next-generation migraine prophylaxis targeting CGRP pathway. Monthly subcutaneous injection."),
        Product(name="GlucoSteady", therapeutic_area="Endocrinology",
                description="GLP-1 receptor agonist for Type 2 Diabetes with cardiovascular benefits."),
        Product(name="BreathEase", therapeutic_area="Pulmonology",
                description="Biologic therapy for severe eosinophilic asthma. Reduces exacerbations by 60%."),
        Product(name="FlexiJoint", therapeutic_area="Rheumatology",
                description="JAK inhibitor for moderate-to-severe rheumatoid arthritis."),
    ]
    db.add_all(products)
    db.commit()

    # ─── Sample Interactions ─────────────────────────────────────────
    interactions = [
        Interaction(
            hcp_id=1, interaction_type="Detail Aid",
            interaction_date=datetime.utcnow() - timedelta(days=5),
            duration_minutes=30, products_discussed="CardioMax",
            key_topics="Efficacy data, dosing protocol, real-world evidence",
            hcp_feedback="Interested in switching patients from warfarin. Wants more RWE data.",
            sentiment="Positive", follow_up_actions="Send Phase III data packet; Schedule follow-up in 2 weeks",
            ai_summary="Productive meeting with Dr. Chen regarding CardioMax. She expressed strong interest in transitioning patients from warfarin and requested additional real-world evidence data.",
            raw_notes="Met with Dr. Chen at her office. She's seen the latest NEJM publication on CardioMax and is impressed with the safety profile. Wants to see more real-world evidence before switching her AF patients from warfarin.",
        ),
        Interaction(
            hcp_id=2, interaction_type="Lunch and Learn",
            interaction_date=datetime.utcnow() - timedelta(days=12),
            duration_minutes=60, products_discussed="OncoShield",
            key_topics="PD-L1 expression, combination therapy, adverse event management",
            hcp_feedback="Concerned about immune-related adverse events in elderly patients.",
            sentiment="Neutral", follow_up_actions="Share elderly patient subgroup analysis; Arrange KOL peer discussion",
            ai_summary="Lunch presentation at Mayo Clinic. Dr. Patel raised valid concerns about irAE management in elderly NSCLC patients. Need to provide targeted safety data.",
            raw_notes="Presented OncoShield at a lunch session with Dr. Patel and 3 fellows. Good engagement but Dr. Patel pushed back on the adverse event profile for patients over 75.",
        ),
        Interaction(
            hcp_id=3, interaction_type="Virtual Meeting",
            interaction_date=datetime.utcnow() - timedelta(days=3),
            duration_minutes=20, products_discussed="GlucoSteady",
            key_topics="CV outcome data, weight management benefits, insurance coverage",
            hcp_feedback="Very enthusiastic about the CV benefits. Already prescribing to select patients.",
            sentiment="Positive", follow_up_actions="Send co-pay assistance program details; Invite to speaker program",
            ai_summary="Virtual call with Dr. Rodriguez. She is already prescribing GlucoSteady and is very positive about the cardiovascular outcomes. Interested in the speaker program.",
            raw_notes="Quick Zoom call. Dr. Rodriguez loves GlucoSteady. She's had 3 patients on it for 6 months with great results. Wants to know about the speaker program.",
        ),
    ]
    db.add_all(interactions)
    db.commit()

    print(f"✅ Seeded: {len(hcps)} HCPs, {len(products)} Products, {len(interactions)} Interactions")
    db.close()


if __name__ == "__main__":
    seed()
