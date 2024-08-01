from fastapi import HTTPException,APIRouter,FastAPI
from database.database import sessionlocal
from passlib.context import CryptContext
from src.models.security import User
from src.schemas.security import UserCredentials
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from dotenv import load_dotenv
import os 
from src.utils.token import create_access_token,decode_token_uname,create_refresh_token

import uuid



pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

oauth_scheme = OAuth2PasswordBearer(tokenUrl="encode_token_id")

access_token = APIRouter(tags=["access_token"])

load_dotenv()
SECRET_KEY = str(os.environ.get("SECRET_KEY"))
ALGORITHM = str(os.environ.get("ALGORITHM"))


#---------------------decode_access_token------------------

@access_token.get("/decode_access_uname")
def decode_uname(token: str):
    uname = decode_token_uname(token)
    return {"uname" : uname}

#------------------decode_refresh_token----------------------------

@access_token.get("/decode_refresh_uname")
def decode_uname(token: str):
    uname = decode_token_uname(token)
    return {"uname" : uname}

#------------------------------char_mapping--------------------------------------


char_mapping = {
    'a': '@', 'b': '#', 'c': '%', 'd': '^', 'e': '&', 'f': '*', 'g': '(', 'h': ')',
    'i': '-', 'j': '=', 'k': '+', 'l': '{', 'm': '}', 'n': '[', 'o': ']', 'p': ':',
    'q': ';', 'r': '"', 's': "'", 't': '<', 'u': '>', 'v': ',', 'w': '.', 'x': '?',
    'y': '/', 'z': '|'
}

reverse_char_mapping = {}
for key in char_mapping:
    reverse_char_mapping[char_mapping[key]] = key


def create_secret(uname: str) -> str:
    secret_format = ''
    for char in uname:
        mapped_char = char_mapping.get(char, char)
        secret_format += mapped_char
    return secret_format


def decode_secret(secret: str) :
    decoded_username = ''
    for char in secret:
        original_char = reverse_char_mapping.get(char, char)
        decoded_username += original_char
    return decoded_username

#--------------------------create_token-------------------------------

@access_token.post("/login")
def create_tokens(uname : str ):
    secret_uname = create_secret(uname)
    access_token = create_access_token(uname)
    refresh_token = create_refresh_token( secret_uname )
    return {"access_token": access_token, "refresh_token": refresh_token}

#------------------------refresh_token-------------------------------

@access_token.post("/refresh_by_new_access_token")
def refresh_token(refresh_token: str):
    
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    secret_uname = payload.get("user_name")

    if secret_uname is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    original_uname = decode_secret(secret_uname)
    new_access_token = create_access_token(original_uname)
    return {"new_access_token": new_access_token}
