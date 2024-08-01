from datetime import datetime,timedelta
from fastapi import HTTPException,status
from dotenv import load_dotenv
import os 
from jose import jwt,JWTError

load_dotenv()
SECRET_KEY = str(os.environ.get("SECRET_KEY"))
ALGORITHM = str(os.environ.get("ALGORITHM"))


#--------------------create_access_refresh_token-------------------------

def create_access_token(uname):
    payload = {
        "user_name": uname,
        "exp": datetime.utcnow() + timedelta(minutes=1),
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print(type(access_token))
    return access_token


#--------------------------create_refresh_token-----------------------

def create_refresh_token(uname) :
  
    payload = {
        "user_name": uname,
        "exp": datetime.utcnow() + timedelta(days=1),  
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return access_token

#----------------------decode username---------------------------

def decode_token_uname(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name = payload.get("user_name")
        if not user_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
            )
        return user_name
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
        )
#--------------------decode_password------------------------

def decode_token_password(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_password = payload.get("user_password")
        if not user_password:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
            )
        return user_password
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
        )
        