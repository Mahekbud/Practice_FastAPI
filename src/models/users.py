from sqlalchemy import Column,String,DateTime,Boolean
from database.database import Base
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "Users"
    
    id = Column(String(50),primary_key=True,default=str(uuid.uuid4()))
    f_name = Column(String(50),nullable=False)
    l_name = Column(String(50),nullable=False)
    u_name = Column(String(50),nullable=False)
    email = Column(String(50),nullable=False)
    phone_no = Column(String(10),nullable=False)
    password = Column(String(70),nullable=False)
    is_deleted = Column(Boolean,default=False)
    is_active = Column(Boolean,default=True)
    created_at = Column(DateTime,default=datetime.now)
    modified_at = Column(DateTime,default=datetime.now,onupdate=datetime.now)
    
    
    