from pydantic import BaseModel

class EmployeeAll(BaseModel):
    emp_name : str
    email : str
    phone_no : str
    position : str
    password : str
    
    
class EmpPass(BaseModel):
    password : str 