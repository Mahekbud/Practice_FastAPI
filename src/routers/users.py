from  fastapi import FastAPI,HTTPException,APIRouter
from database.database import Sessionlocal
from passlib.context import CryptContext
from src.schemas.user import UserAll,UserResponse,UserPass,ForgetPass,ResetPass
from src.models.users import User
import uuid
from src.utils.token import get_token,decode_token_user_id,decode_token_user_email,decode_token_uname,get_token_login,decode_token_password



pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

Users = APIRouter()

db = Sessionlocal()

#-------------------------------create user-------------------------------

@Users.post("/create_user/",response_model=UserAll)
def create_user(user:UserAll):
    new_user= User(
        id = str(uuid.uuid4()),
        f_name = user.f_name,
        l_name = user.l_name,
        u_name = user.u_name,
        email = user.email,
        phone_no = user.phone_no,
        password = pwd_context.hash(user.password)
    )
    db.add(new_user)
    db.commit()
    return new_user

# --------------------------------get by id--------------------------------------

@Users.get("/get_user_by_id",response_model=UserResponse)
def get_user_by_id(user_id:str):
    users = db.query(User).filter(User.id == user_id , User.is_active == True).first()
    if users is  None:
        raise HTTPException(status_code=404,detail="user not found")
    return users

#---------------------------------get by id token--------------------------------------


@Users.get("/get_token_id",response_model=UserResponse)
def get_user_token_id(token:str):
    user_id = decode_token_user_id(token)
    users = db.query(User).filter(User.id == user_id , User.is_active == True).first()
    if users is  None:
        raise HTTPException(status_code=404,detail="user not found")
    return users

# ---------------------------------all user-------------------------------------

@Users.get("/get_all_user",response_model=list[UserAll])
def get_all_user():
    users = db.query(User).all()
    if users is  None:
        raise HTTPException(status_code=404,detail="user not found")
    return users



#--------------------------------update-------------------------------------

@Users.put("/update_user",response_model=UserAll)
def update_User(user_id:str,user1:UserAll):
    users = db.query(User).filter(User.id == user_id , User.is_active == True).first()
    if users is  None:
        raise HTTPException(status_code=404,detail="user not found")
    
    users.f_name = user1.f_name,
    users.l_name = user1.l_name,
    users.u_name = user1.u_name
    users.email = user1.email,
    users.phone_no = user1.phone_no,
    users.password = pwd_context.hash(users.password),
    
    db.commit()
    return users

#-------------------------------update_token----------------------------

@Users.put("/update_user_token",response_model=UserAll)
def update_User(token:str,user1:UserAll):
    user_id = decode_token_user_id(token)
    users = db.query(User).filter(User.id == user_id , User.is_active == True).first()
    if users is  None:
        raise HTTPException(status_code=404,detail="user not found")
    
    users.f_name = user1.f_name,
    users.l_name = user1.l_name,
    users.u_name = user1.u_name
    users.email = user1.email,
    users.phone_no = user1.phone_no,
    users.password = pwd_context.hash(users.password),
    
    db.commit()
    return users


#  ----------------------------Delete---------------------------------------

@Users.delete("/delete_user")
def delete_user(User_id:str):
    db_user = db.query(User).filter(User.id == User_id , User.is_active == True).first()
    if db_user is None:
        raise HTTPException(status_code=404,detail="User not found")
    
    db_user.is_active = False
    db_user.is_deleted = True

    db.commit()
    return {"message":"user deleted successfully"}

#----------------------------delete_token---------------------------------

@Users.delete("/delete_user_token/")
def delete_user(token :str):
    User_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == User_id , User.is_active == True).first()
    if db_user is None:
        raise HTTPException(status_code=404,detail="User not found")
    
    db_user.is_active = False
    db_user.is_deleted = True

    db.commit()
    return {"message":"user deleted successfully"}

# ---------------------------------Reregister--------------------------------

@Users.put("/reregister_user")
def rergister_users(user_id: str, user1: UserPass):
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if db_user.is_deleted is True and db_user.is_active is False:
        if pwd_context.verify(user1.password, db_user.password):
       
            db_user.is_deleted = False
            db_user.is_active = True
            db.commit()  
            return True 
 
    raise HTTPException(status_code=401, detail="Invalid credentials")

# -------------------------------forgetpassword---------------------------------

@Users.put("/forget_password")
def forget_Password(user_email : str ,user_newpass : str):
    db_users = db.query(User).filter(User.email == user_email ).first()
    if db_users is  None:
        raise HTTPException(status_code=404,detail="user not found")
    
    db_users.password = pwd_context.hash(user_newpass)
    
    db.commit()
    return "Forget Password successfully"

#-------------------------------forget_password_token--------------------------

@Users.put("/forget_password_token")
def forget_Password(token : str ,user_newpass : str):
    user_email = decode_token_user_email(token)
    db_users = db.query(User).filter(User.email == user_email ).first()
    if db_users is  None:
        raise HTTPException(status_code=404,detail="user not found")
    
    db_users.password = pwd_context.hash(user_newpass)
    
    db.commit()
    return "Forget Password successfully"


# -------------------------------ResetPassword----------------------------------


@Users.put("/reset_password")
def reset_password(user_email: str, user_oldpass: str, user_newpass: str):
    db_user = db.query(User).filter(User.email == user_email).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if pwd_context.verify(user_oldpass , db_user.password):
        db_user.password = pwd_context.hash(user_newpass)
        db.commit()
        return "Password reset successfully"
    else:
        return "old password not matched"
    
#-----------------------------reset password token---------------------------
    
@Users.put("/reset_password_token")
def reset_password_token(token: str, user_oldpass: str, user_newpass: str):
    user_email = decode_token_user_email(token)
    db_user = db.query(User).filter(User.email == user_email).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if pwd_context.verify(user_oldpass , db_user.password):
        db_user.password = pwd_context.hash(user_newpass)
        db.commit()
        return "Password reset successfully"
    else:
        return "old password not matched"
    
 #--------------------------------Encode Token---------------------------  

@Users.get("/encode_token")
def encode_token(id : str , email : str ,uname : str  ):
    access_token = get_token(id,email,uname)
    return access_token 


# ---------------------------------Encode_login-----------------------------------

@Users.get("/encode_login")
def encode_login(u_name : str , password : str):
    access_token = get_token_login(u_name,password)
    return access_token

#  -------------- Decode email-------------------

@Users.get("/decode_email")
def decode_email(token: str):
    email = decode_token_user_email(token)
    return email

# ---------------- Decode_id -------------------

@Users.get("/decode_id")
def decode_id(token : str):
    id = decode_token_user_id(token)
    return id

# ----------------- Decode_uname -----------------

@Users.get("/decode_uname")
def decode_uname(token : str):
    id = decode_token_uname(token)
    return id

#------------------Decode_password-------------------

@Users.get("/decode_password")
def decode_password(token : str):
    password = decode_token_password(token)
    return password

#---------------------all token------------------------

@Users.get("/decode")
def decode(token : str):
    id = decode_token_user_id(token)
    email = decode_token_user_email(token)
    uname = decode_token_uname(token)
    return id,email,uname

#------------------------------------login------------------------------------


@Users.get("/login")
def login( uname: str,password: str):
    db_user = db.query(User).filter(User.u_name == uname,User.is_active == True).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not pwd_context.verify(password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
   
    return "Login successful"


#----------------------------------login_token-----------------------------------

@Users.get("/login_token")
def login_token(token : str):
    uname = decode_token_uname(token)
    password = decode_token_password(token)
    db_user = db.query(User).filter(User.u_name == uname,User.is_active == True).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not pwd_context.verify(password,db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
   
    return "Login successful"















