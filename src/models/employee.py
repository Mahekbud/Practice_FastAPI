from sqlalchemy import Column,String,Boolean,DateTime
from database.database import Base
import uuid
from datetime import datetime

class employee(Base):
    __tablename__ = "employee_details"
    
    id = Column(String(50),primary_key=True,default=str(uuid.uuid4()))
    emp_name = Column(String(50),nullable=False)
    email = Column(String(50),nullable=False)
    phone_no = Column(String(10),nullable=False)
    position = Column(String(50),nullable=False)
    password = Column(String(80),nullable=False)
    is_active = Column(Boolean,default=True)
    is_delete = Column(Boolean,default=False)
    created_at = Column(DateTime,default=datetime.now)
    modified_at = Column(DateTime,default=datetime.now,onupdate=datetime.now)