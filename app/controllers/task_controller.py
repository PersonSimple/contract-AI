from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.task import Task
from app.models.contract import Contract
from app.models.contractor import Contractor
from app.models.cost import Cost

from app.models.schemas import TaskCreate, TaskResponse

from app.services.cost_service import calculate_cost
from app.services.contract_service import validate_budget
from app.exceptions.custom_exceptions import BudgetExceededException


router = APIRouter(prefix="/tasks", tags=["Tasks"])


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):

    # Check contract exists
    contract = db.query(Contract).filter(
        Contract.id == task.contract_id
    ).first()

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    new_task = Task(
        task_name=task.task_name,
        contract_id=task.contract_id,
        estimated_hours=task.estimated_hours,
        status="PENDING"
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task



@router.get("/contract/{contract_id}")
def get_tasks(contract_id: int, db: Session = Depends(get_db)):

    tasks = db.query(Task).filter(
        Task.contract_id == contract_id
    ).all()

    return tasks



@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_status(task_id: int, status: str, db: Session = Depends(get_db)):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Validate status
    valid_status = ["PENDING", "IN_PROGRESS", "COMPLETED"]
    if status not in valid_status:
        raise HTTPException(status_code=400, detail="Invalid status")

    task.status = status

    
    if status == "COMPLETED":

        # Prevent duplicate cost creation
        if len(task.costs) > 0:
            db.commit()
            db.refresh(task)
            return task

        # Get contract
        contract = db.query(Contract).filter(
            Contract.id == task.contract_id
        ).first()

        # Get contractor
        contractor = db.query(Contractor).filter(
            Contractor.id == contract.contractor_id
        ).first()

        # Use estimated hours as final hours
        hours = task.estimated_hours

        # Calculate cost
        total_cost = calculate_cost(hours, contractor.hourly_rate)

        # Validate budget
        try:
            validate_budget(contract, total_cost)
        except BudgetExceededException as e:
            raise HTTPException(status_code=400, detail=str(e))

        # Create cost entry
        new_cost = Cost(
            task_id=task.id,
            hours_worked=hours,
            hourly_rate=contractor.hourly_rate,
            total_cost=total_cost
        )

        # Update actual hours
        task.actual_hours = hours

        db.add(new_cost)

    db.commit()
    db.refresh(task)

    return task