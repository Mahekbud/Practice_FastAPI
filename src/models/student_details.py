

from sqlalchemy import String,Integer,DateTime,Boolean,Column,Float
from sqlalchemy.orm import relationship
from database.database import Base
import uuid
from datetime import datetime,timezone




class Stu(Base):
    __tablename__="students"
    
    id = Column(String(50),primary_key=True,default=str(uuid.uuid4()))
    f_name = Column(String(100),nullable = False)
    m_name = Column(String(100),nullable = False)
    l_name = Column(String(100),nullable = False)
    roll_no = Column(String(50),unique = True)
    age = Column(String(10),nullable = False)
    email = Column(String(50),nullable = False)
    phone_no = Column(String(10))
    address = Column(String(200),nullable = False)
    branch = Column(String(100),nullable = False)
    dob =Column(String(20),nullable = False)
    admission_date = Column(String(50))
    gender = Column(String(50),nullable = False)
    adharcard_no = Column(String(12),nullable = False) 
    cast = Column(String(50),nullable = False)
    state = Column(String(50),nullable = False)
    fees = Column(String(10),nullable = False)
    hsc_percentage = Column(Float(10),nullable = False)
    create_at = Column(DateTime,default=datetime.now())
    modified_at = Column(DateTime,default=datetime.now() ,onupdate=datetime.now())
    is_active = Column(Boolean,default=True)
    is_deleted = Column(Boolean,default = False)
    

    
# {
#   "f_name": "mahek",
#   "m_name": "jayntibhai",
#   "l_name": "bud",
#   "roll_no": "32",
#   "age": "21",
#   "email": "mahekbud@gmail.com",
#   "phone_no": "2323232323",
#   "address": "surat",
#   "branch": "ce",
#   "dob": "12/34/5666",
#   "admission_date": "23/34/5464",
#   "gender": "female",
#   "adharcard_no": "233434334134",
#   "cast": "kp",
#   "state": "gujarat",
#   "fees": "23000",
#   "hsc_percentage": 2.3
# }