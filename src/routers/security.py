from fastapi import HTTPException,APIRouter,FastAPI
from database.database import sessionlocal
from passlib.context import CryptContext
from src.models.security import User
from src.schemas.security import passwordnormal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import uuid



pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

oauth_scheme = OAuth2PasswordBearer(tokenUrl="encode_token_id")

securitysystem = APIRouter()

db = sessionlocal()

#-------------------------create password-----------------------


@securitysystem.post("/create_password",response_model=passwordnormal)
def create_password(security : passwordnormal):
        # modified_password = security.password + "@$259"   
    
        # hashed_password = pwd_context.hash(modified_password)
        
        new_pass = User(
              id = str(uuid.uuid4()),
              u_name = security.u_name,
              password = security.password       
       )          
        db.add(new_pass)
        db.commit()
        return new_pass
  
#---------------------------login------------------
    
@securitysystem.get("/login")
def login (u_name : str,password : str ):
    db_pass = db.query(User).filter(User.u_name == u_name,User.is_active==True).first()
    modified_passwords = password + "@$259" 
    if db_pass is None : 
        raise HTTPException(status_code=404,detail="pass not found")
    
    if not pwd_context.verify(modified_passwords,db_pass.password):
        raise HTTPException(status_code=401,detail="incorrect password")
    
    return "login successfully"

#--------------------------unique password---------------------------------

@securitysystem.post("/create_password_unique",response_model=passwordnormal)
def create_password_unique(security : passwordnormal):
    char_mapping = {
    'a': '@', 'b': '#', 'c': '%', 'd': '^', 'e': '&', 'f': '*', 'g': '(', 'h': ')',
    'i': '-', 'j': '=', 'k': '+', 'l': '{', 'm': '}', 'n': '[', 'o': ']', 'p': ':',
    'q': ';', 'r': '"', 's': "'", 't': '<', 'u': '>', 'v': ',', 'w': '.', 'x': '?',
    'y': '/', 'z': '|'
            }
    new_password = ""
    for char in security.password:
        new_password += char_mapping.get(char.lower(), char)
        
    new_passwords =  security.password + "@$259" + new_password
    
    # sliceing_pass = "@$259" + new_password
    
    # new_passs = security.password[:2] + sliceing_pass + security.password[2:]
    
    new_pass = User(
              u_name = security.u_name,
              password = new_passwords   
        )   
           
    db.add(new_pass)
    db.commit()
    return new_pass
 #--------------------------------unique password login------------------------------------
 
    
@securitysystem.get("/login_unique")
def login_unique (u_name : str,password : str ):
    
    db_pass = db.query(User).filter(User.u_name == u_name,User.is_active == True).first()
    
    if db_pass is None : 
        raise HTTPException(status_code=404,detail="pass not found")
    
    char_mapping = {
    'a': '@', 'b': '#', 'c': '%', 'd': '^', 'e': '&', 'f': '*', 'g': '(', 'h': ')',
    'i': '-', 'j': '=', 'k': '+', 'l': '{', 'm': '}', 'n': '[', 'o': ']', 'p': ':',
    'q': ';', 'r': '"', 's': "'", 't': '<', 'u': '>', 'v': ',', 'w': '.', 'x': '?',
    'y': '/', 'z': '|'
            }
    new_password = ""
    for char in password:
        new_password += char_mapping.get(char.lower(), char)
        
    new_passwords = password + "@$259" + new_password
    
    if not pwd_context.verify(new_passwords,db_pass.password):
        raise HTTPException(status_code=401,detail="incorrect password")
    
    return "login successfully"

#------------------------------unique password use by ABCD,abcd ------------------------

# @securitysystem.post("/create_password_unique_lower_upper",response_model=passwordnormal)
# def create_password_unique(security : passwordnormal):
#     char_mapping = {
#     'a': '@', 'b': '#', 'c': '%', 'd': '^', 'e': '&', 'f': '*', 'g': '(', 'h': ')',
#     'i': '-', 'j': '=', 'k': '+', 'l': '{', 'm': '}', 'n': '[', 'o': ']', 'p': ':',
#     'q': ';', 'r': '"', 's': "'", 't': '<', 'u': '>', 'v': ',', 'w': '.', 'x': '?',
#     'y': '/', 'z': '|',
#     'A': '!', 'B': '~', 'C': '`', 'D': '|', 'E': '\\', 'F': '/', 'G': '_', 'H': '.',
#     'I': ',', 'J': '{', 'K': '}', 'L': '[', 'M': ']', 'N': '<', 'O': '>', 'P': ':',
#     'Q': ';', 'R': '"', 'S': "'", 'T': '?', 'U': '|', 'V': '`', 'W': '~', 'X': '!',
#     'Y': '@', 'Z': '#'
#             }
#     new_password = ""
#     for char in security.password:
#         new_password += char_mapping.get(char, char)
    
#     new_passwords = security.password + "@$259" + new_password 
    
#     new_pass = User(
#               u_name = security.u_name,
#               password =  pwd_context.hash(new_passwords)
#         )   
           
#     db.add(new_pass)
#     db.commit()
#     return new_pass

#---------------------------unique_lower_upper_digit--------------------------------------

@securitysystem.post("/create_password_unique_lower_upper_digit",response_model=passwordnormal)
def create_password_unique_digit(security : passwordnormal):
    char_mapping = {
    'a': '@', 'b': '#', 'c': '%', 'd': '^', 'e': '&', 'f': '*', 'g': '(', 'h': ')',
    'i': '-', 'j': '=', 'k': '+', 'l': '{', 'm': '}', 'n': '[', 'o': ']', 'p': ':',
    'q': ';', 'r': '"', 's': "'", 't': '<', 'u': '>', 'v': ',', 'w': '.', 'x': '?',
    'y': '/', 'z': '|',
    'A': '!', 'B': '~', 'C': '`', 'D': '|', 'E': '\\', 'F': '/', 'G': '_', 'H': '.',
    'I': ',', 'J': '{', 'K': '}', 'L': '[', 'M': ']', 'N': '<', 'O': '>', 'P': ':',
    'Q': ';', 'R': '"', 'S': "'", 'T': '?', 'U': '|', 'V': '`', 'W': '~', 'X': '!',
    'Y': '@', 'Z': '#'
            }
    new_password = ""
    for char in security.password:
        if char.isalpha():  
            new_password += char_mapping.get(char, char)
        else:
            new_password += char
        
    new_passwords =  security.password + "@$259" + new_password
    
    new_pass = User(
              u_name = security.u_name,
              password = pwd_context.hash(new_passwords)
        )   
           
    db.add(new_pass)
    db.commit()
    return new_pass
#----------------------------------login upper lower --------------------------- 


# @securitysystem.get("/login_unique_char_digit")
# def login_unique_char_digit (u_name : str,password : str ):
    
#     db_pass = db.query(User).filter(User.u_name == u_name,User.is_active == True).first()
    
#     if db_pass is None : 
#         raise HTTPException(status_code=404,detail="pass not found")
    
#     char_mapping = {
#     'a': '@', 'b': '#', 'c': '%', 'd': '^', 'e': '&', 'f': '*', 'g': '(', 'h': ')',
#     'i': '-', 'j': '=', 'k': '+', 'l': '{', 'm': '}', 'n': '[', 'o': ']', 'p': ':',
#     'q': ';', 'r': '"', 's': "'", 't': '<', 'u': '>', 'v': ',', 'w': '.', 'x': '?',
#     'y': '/', 'z': '|',
#     'A': '!', 'B': '~', 'C': '`', 'D': '|', 'E': '\\', 'F': '/', 'G': '_', 'H': '.',
#     'I': ',', 'J': '{', 'K': '}', 'L': '[', 'M': ']', 'N': '<', 'O': '>', 'P': ':',
#     'Q': ';', 'R': '"', 'S': "'", 'T': '?', 'U': '|', 'V': '`', 'W': '~', 'X': '!',
#     'Y': '@', 'Z': '#'
#     }
#     new_password = ""
#     for char in password:
#             new_password += char_mapping.get(char, char)
        
#     new_passwords =  password + "@$259" + new_password
    
#     if not pwd_context.verify(new_passwords,db_pass.password):
#         raise HTTPException(status_code=401,detail="incorrect password")
    
#     return "login successfully"

#------------------------------------unique_lower_upper_digit_login --------------------------------------

@securitysystem.get("/login_unique_char_digit")
def login_unique_char_digit (u_name : str,password : str ):
    
    db_pass = db.query(User).filter(User.u_name == u_name,User.is_active == True).first()
    
    if db_pass is None : 
        raise HTTPException(status_code=404,detail="pass not found")
    
    char_mapping = {
    'a': '@', 'b': '#', 'c': '%', 'd': '^', 'e': '&', 'f': '*', 'g': '(', 'h': ')',
    'i': '-', 'j': '=', 'k': '+', 'l': '{', 'm': '}', 'n': '[', 'o': ']', 'p': ':',
    'q': ';', 'r': '"', 's': "'", 't': '<', 'u': '>', 'v': ',', 'w': '.', 'x': '?',
    'y': '/', 'z': '|',
    'A': '!', 'B': '~', 'C': '`', 'D': '|', 'E': '\\', 'F': '/', 'G': '_', 'H': '.',
    'I': ',', 'J': '{', 'K': '}', 'L': '[', 'M': ']', 'N': '<', 'O': '>', 'P': ':',
    'Q': ';', 'R': '"', 'S': "'", 'T': '?', 'U': '|', 'V': '`', 'W': '~', 'X': '!',
    'Y': '@', 'Z': '#'
            }
    new_password = ""
    for char in password:
         if char.isalpha():  
            new_password += char_mapping.get(char, char)
         else:
            new_password += char
        
    new_passwords =  password + "@$259" + new_password
    
    if not pwd_context.verify(new_passwords,db_pass.password):
        raise HTTPException(status_code=401,detail="incorrect password")
    
    return "login successfully"

