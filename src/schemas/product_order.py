from pydantic import BaseModel

class OrderAll(BaseModel):
    product_id : int
    quantity : int
    
class ProductAll(BaseModel):
    name : str 
    price : int
    
class productpass(BaseModel):
    name : str
    
class orderid(BaseModel):
    id :int