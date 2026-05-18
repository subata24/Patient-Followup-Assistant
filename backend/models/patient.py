from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text)
    discharge_summary = Column(Text)
    risk_level = Column(Text)