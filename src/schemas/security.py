from pydantic import BaseModel

class passwordnormal(BaseModel):
    u_name : str
    password : str
    
class UserCredentials(BaseModel):
    uname: str
    password: str