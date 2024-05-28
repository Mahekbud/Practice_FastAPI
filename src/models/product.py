from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Boolean
from datetime import datetime
import uuid

from database.database import Base

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String)
    price = Column(Integer)
    is_active = Column(Boolean,default=True)
    is_delete = Column(Boolean,default=False)
    created_at = Column(DateTime,default=datetime.now)
    modified_at = Column(DateTime,default=datetime.now,onupdate=datetime.now)