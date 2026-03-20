from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.contract import Contract
from app.models.contractor import Contractor
from app.models.schemas import ContractCreate, ContractResponse

router = APIRouter(prefix="/contracts", tags=["Contracts"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ContractResponse)
def create_contract(contract: ContractCreate, db: Session = Depends(get_db)):

    # Check contractor exists
    contractor = db.query(Contractor).filter(
        Contractor.id == contract.contractor_id
    ).first()

    if not contractor:
        raise HTTPException(status_code=404, detail="Contractor not found")

    # Validate budget
    if contract.max_budget <= 0:
        raise HTTPException(status_code=400, detail="Budget must be greater than zero")

    new_contract = Contract(
        contract_name=contract.contract_name,
        contractor_id=contract.contractor_id,
        start_date=contract.start_date,
        end_date=contract.end_date,
        max_budget=contract.max_budget,
        status=contract.status
    )

    db.add(new_contract)
    db.commit()
    db.refresh(new_contract)

    return new_contract


@router.get("/", response_model=list[ContractResponse])
def get_contracts(db: Session = Depends(get_db)):
    return db.query(Contract).all()


@router.get("/{contract_id}", response_model=ContractResponse)
def get_contract(contract_id: int, db: Session = Depends(get_db)):

    contract = db.query(Contract).filter(Contract.id == contract_id).first()

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    return contract

from app.services.contract_service import calculate_progress


@router.get("/{contract_id}/summary")
def get_contract_summary(contract_id: int, db: Session = Depends(get_db)):

    contract = db.query(Contract).filter(Contract.id == contract_id).first()

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    # total cost
    total_cost = sum(
        cost.total_cost
        for task in contract.tasks
        for cost in task.costs
    )

    # remaining budget
    remaining_budget = contract.max_budget - total_cost

    # progress
    progress = calculate_progress(contract)

    return {
        "contract_id": contract.id,
        "contract_name": contract.contract_name,
        "total_cost": total_cost,
        "remaining_budget": remaining_budget,
        "progress": progress
    }