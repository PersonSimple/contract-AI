from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    task_name = Column(String, nullable=False)

    contract_id = Column(Integer, ForeignKey("contracts.id"))

    estimated_hours = Column(Float, nullable=False)
    actual_hours = Column(Float, default=0)

    status = Column(String, default="PENDING")

    contract = relationship("Contract", back_populates="tasks")

    costs = relationship(
        "Cost",
        back_populates="task",
        cascade="all, delete-orphan"
    )