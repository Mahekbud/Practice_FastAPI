from pydantic import BaseModel

class UserAll(BaseModel):
    f_name : str
    l_name : str
    u_name : str
    email : str
    phone_no : str
    password : str
    
    
class UserResponse(BaseModel):
    f_name : str
    l_name : str
    u_name : str
    email : str
    phone_no : str

class UserPass(BaseModel):
    password : str
    
class ForgetPass(BaseModel):
    password : str
    
class ResetPass(BaseModel):
    email : str
    password : str
    
class login(BaseModel):
    email : str
    