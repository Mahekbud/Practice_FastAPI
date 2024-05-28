from database.database import Base
from sqlalchemy import String,Integer,ForeignKey,Column,Boolean,DateTime
from datetime import datetime


class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer,primary_key=True,autoincrement=True)
    product_id = Column(Integer,ForeignKey('products.id'))
    quantity = Column(Integer)
    is_active = Column(Boolean,default=True)
    is_delete = Column(Boolean,default=False)
    created_at = Column(DateTime,default=datetime.now)
    modified_at = Column(DateTime,default=datetime.now,onupdate=datetime.now)