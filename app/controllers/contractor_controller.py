from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.contractor import Contractor
from app.models.schemas import ContractorCreate, ContractorResponse

router = APIRouter(prefix="/contractors", tags=["Contractors"])


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Contractor
from app.models.schemas import ContractorCreate, ContractorResponse


@router.post("/", response_model=ContractorResponse)
def create_contractor(contractor: ContractorCreate, db: Session = Depends(get_db)):

    if contractor.hourly_rate <= 0:
        raise HTTPException(status_code=400, detail="Hourly rate must be positive")

    new_contractor = Contractor(
        name=contractor.name,
        email=contractor.email,
        skill=contractor.skill,
        hourly_rate=contractor.hourly_rate
    )

    db.add(new_contractor)
    db.commit()
    db.refresh(new_contractor)

    return new_contractor


# Get All Contractors
@router.get("/")
def get_contractors(db: Session = Depends(get_db)):
    return db.query(Contractor).all()


# Get Contractor by ID
@router.get("/{contractor_id}")
def get_contractor(contractor_id: int, db: Session = Depends(get_db)):

    contractor = db.query(Contractor).filter(Contractor.id == contractor_id).first()

    if not contractor:
        raise HTTPException(status_code=404, detail="Contractor not found")

    return contractor

