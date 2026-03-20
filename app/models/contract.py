from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    contract_name = Column(String, nullable=False)

    contractor_id = Column(Integer, ForeignKey("contractors.id"))

    start_date = Column(Date)
    end_date = Column(Date)

    max_budget = Column(Float, nullable=False)
    status = Column(String)

    contractor = relationship("Contractor", back_populates="contracts")
    tasks = relationship("Task", back_populates="contract")