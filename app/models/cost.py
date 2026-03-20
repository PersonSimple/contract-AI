from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Cost(Base):
    __tablename__ = "costs"

    id = Column(Integer, primary_key=True, index=True)

    task_id = Column(Integer, ForeignKey("tasks.id"))

    hours_worked = Column(Float, nullable=False)
    hourly_rate = Column(Float, nullable=False)

    total_cost = Column(Float, nullable=False)

    date = Column(Date)

    task = relationship("Task", back_populates="costs")