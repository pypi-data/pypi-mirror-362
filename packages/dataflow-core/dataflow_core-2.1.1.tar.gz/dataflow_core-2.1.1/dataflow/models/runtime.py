from sqlalchemy import Column, Integer, String, Boolean
from dataflow.db import Base

class RuntimeZone(Base):
    __tablename__ = "RUNTIME_ZONE"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=False)
    display_order = Column(Integer)
    spark_enabled = Column(Boolean, default=False)
