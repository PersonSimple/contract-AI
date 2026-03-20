from fastapi import FastAPI
from app.database import Base, engine

# Import models so SQLAlchemy can detect them
from app.models import contractor, contract, task, cost

app = FastAPI(title="Contract AI Management System")

# Create database tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Contract AI system running"}

from app.controllers import contractor_controller

app.include_router(contractor_controller.router)


from app.controllers import contract_controller

app.include_router(contract_controller.router)


from app.controllers import task_controller

app.include_router(task_controller.router)

from app.controllers import cost_controller
app.include_router(cost_controller.router)


from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import (
    BudgetExceededException,
    TaskNotFoundException,
    ContractNotFoundException,
    InvalidHoursException
)


@app.exception_handler(BudgetExceededException)
async def budget_handler(request: Request, exc: BudgetExceededException):
    return JSONResponse(
        status_code=400,
        content={"error": "BudgetExceededException", "message": exc.message}
    )


@app.exception_handler(TaskNotFoundException)
async def task_handler(request: Request, exc: TaskNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"error": "TaskNotFoundException", "message": exc.message}
    )


@app.exception_handler(ContractNotFoundException)
async def contract_handler(request: Request, exc: ContractNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"error": "ContractNotFoundException", "message": exc.message}
    )


@app.exception_handler(InvalidHoursException)
async def hours_handler(request: Request, exc: InvalidHoursException):
    return JSONResponse(
        status_code=400,
        content={"error": "InvalidHoursException", "message": exc.message}
    )


from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import (
    BudgetExceededException,
    TaskNotFoundException,
    ContractNotFoundException,
    InvalidHoursException
)


@app.exception_handler(BudgetExceededException)
async def budget_handler(request: Request, exc: BudgetExceededException):
    return JSONResponse(
        status_code=400,
        content={
            "error": "BudgetExceededException",
            "message": exc.message
        }
    )


@app.exception_handler(TaskNotFoundException)
async def task_handler(request: Request, exc: TaskNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "error": "TaskNotFoundException",
            "message": exc.message
        }
    )


@app.exception_handler(ContractNotFoundException)
async def contract_handler(request: Request, exc: ContractNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "error": "ContractNotFoundException",
            "message": exc.message
        }
    )


@app.exception_handler(InvalidHoursException)
async def hours_handler(request: Request, exc: InvalidHoursException):
    return JSONResponse(
        status_code=400,
        content={
            "error": "InvalidHoursException",
            "message": exc.message
        }
    )