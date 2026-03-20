from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base


class Contractor(Base):
    __tablename__ = "contractors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String)
    skill = Column(String)
    hourly_rate = Column(Float, nullable=False)

    contracts = relationship("Contract", back_populates="contractor")