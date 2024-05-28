from datetime import datetime,timedelta
from fastapi import HTTPException,status
from dotenv import load_dotenv
import os 
from jose import jwt,JWTError
load_dotenv()
SECRET_KEY = str(os.environ.get("SECRET_KEY"))
ALGORITHM = str(os.environ.get("ALGORITHM"))



def get_token_product(id,name,price):
    payload = {
        "product_id" : id,
        "product_name": name,
        "product_price" : price,
        "exp" : datetime.now() + timedelta(minutes=10)
    }
    
    access_token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    print(type(access_token))
    return access_token



def get_token_product_by_id(id):
    payload = {
        "product_id" : id,
        "exp" : datetime.now() + timedelta(hours=1)
    }
    access_token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    print(type(access_token))
    return access_token



def decode_token_by_product_id(token):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        product_id = payload.get("product_id")
        if not product_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Product ID not found in token"
            )
        return product_id
    except JWTError :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"
        )
        

def get_token_order_by_id(id):
    payload = {
        "order_id" : id,
        "exp" : datetime.now() + timedelta(minutes=10)
    }
    access_token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    print(type(access_token))
    return access_token

def decode_token_by_order_id(token):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        order_id = payload.get("order_id")
        if not order_id:
             raise HTTPException(
                 status_code=status.HTTP_403_FORBIDDEN,
                 detail="order id not found in token"
             )
        return order_id
    except JWTError :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="invalid token"
        )
        
        