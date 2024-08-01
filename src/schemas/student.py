from pydantic import BaseModel
from datetime import datetime

class Student(BaseModel):
    f_name : str
    m_name : str
    l_name : str
    roll_no : str
    age : str
    email : str
    phone_no : str
    address : str
    branch : str
    dob : str
    admission_date : str
    gender : str
    adharcard_no : str
    cast : str
    state : str
    fees : str
    hsc_percentage : float


class StuBase(BaseModel):
    f_name : str
    m_name : str
    l_name : str
    roll_no : str
    phone_no : str
    branch : str
    gender : str
    
  