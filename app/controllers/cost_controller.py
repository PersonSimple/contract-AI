from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.cost import Cost
from app.models.task import Task
from app.models.contract import Contract
from app.models.contractor import Contractor

from app.services.cost_service import calculate_cost
from app.services.contract_service import validate_budget
from app.exceptions.custom_exceptions import BudgetExceededException

from app.models.schemas import CostResponse

router = APIRouter(prefix="/costs", tags=["Costs"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CostResponse)
def add_cost(task_id: int, hours: float, db: Session = Depends(get_db)):

    # Validation
    if hours <= 0:
        raise HTTPException(status_code=400, detail="Hours must be positive")

    # Get task
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Get contract
    contract = db.query(Contract).filter(Contract.id == task.contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    # Get contractor
    contractor = db.query(Contractor).filter(
        Contractor.id == contract.contractor_id
    ).first()
    if not contractor:
        raise HTTPException(status_code=404, detail="Contractor not found")

    # Calculate cost
    total_cost = calculate_cost(hours, contractor.hourly_rate)

    # Validate budget
    try:
        validate_budget(contract, total_cost)
    except BudgetExceededException as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Create cost entry
    new_cost = Cost(
        task_id=task_id,
        hours_worked=hours,
        hourly_rate=contractor.hourly_rate,
        total_cost=total_cost
    )

    # Update actual hours
    task.actual_hours += hours

    db.add(new_cost)
    db.commit()
    db.refresh(new_cost)

    return new_cost