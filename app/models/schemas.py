from pydantic import BaseModel, Field
from datetime import date


# ---------------- Contractor ----------------
class ContractorCreate(BaseModel):
    name: str
    email: str
    skill: str
    hourly_rate: float = Field(gt=0)


class ContractorResponse(BaseModel):
    id: int
    name: str
    email: str
    skill: str
    hourly_rate: float

    class Config:
        from_attributes = True


# ---------------- Contract ----------------
class ContractCreate(BaseModel):
    contract_name: str
    contractor_id: int
    start_date: date
    end_date: date
    max_budget: float = Field(gt=0)
    status: str


class ContractResponse(BaseModel):
    id: int
    contract_name: str
    contractor_id: int
    start_date: date
    end_date: date
    max_budget: float
    status: str

    class Config:
        from_attributes = True


# ---------------- Task ----------------
class TaskCreate(BaseModel):
    task_name: str
    contract_id: int
    estimated_hours: float = Field(ge=0)


class TaskResponse(BaseModel):
    id: int
    task_name: str
    contract_id: int
    estimated_hours: float
    actual_hours: float
    status: str

    class Config:
        from_attributes = True


# ---------------- Cost ----------------
class CostResponse(BaseModel):
    id: int
    task_id: int
    hours_worked: float
    hourly_rate: float
    total_cost: float

    class Config:
        from_attributes = True