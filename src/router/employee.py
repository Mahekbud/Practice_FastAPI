from fastapi import HTTPException,APIRouter,FastAPI,Depends,Header
from database.database import sessionlocal
from passlib.context import CryptContext
from src.schemas.employee import EmployeeAll,EmpPass
from src.models.employee import employee
import uuid
from src.utils.token import get_token,decode_token_emp_id,get_token_login,decode_token_emp_name,decode_token_password
from logs.log_config import logger



pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

employees = APIRouter()

db = sessionlocal()

#---------------------------Create employee-----------------------------

@employees.post("/create_employee",response_model=EmployeeAll)
def create_employee(emp : EmployeeAll):
    logger.info("employee is creating.....")
    new_emp = employee(
        id = str(uuid.uuid4()),
        emp_name = emp.emp_name,
        email = emp.email,
        phone_no = emp.phone_no,
        position = emp.position,
        password = pwd_context.hash(emp.password)  
    )
    logger.success("employee is created.")
    logger.info("employee adding to database.......")
    db.add(new_emp)
    logger.info("employee loaded successfully")
    db.commit()
    logger.success("database has been saved successfully.")
    return new_emp

#--------------------------id token-----------------------------

@employees.get("/encode_token_id")
def encode_token_id(id : str ):
    logger.info(f"access token genereting....{id}")
    access_token = get_token(id)
    logger.info(f"access token genereted:{id}")
    logger.success("access token successfully.")
    return access_token

#-----------------------get by id token-------------------------

@employees.get("/get_id_by_token",response_model=EmployeeAll)
def get_id_by_token(token : str):
    logger.info("accessing employee by token")
    emp_id = decode_token_emp_id(token)
    logger.info("Decoded employee ID from token")
    db_emp = db.query(employee).filter(employee.id == emp_id, employee.is_active == True).first()
    logger.success("retrieved  employee successfully")
    if db_emp is None:
        logger.error("Employee not found")
        raise HTTPException (status_code=404,detail="emp not found")
    
    logger.info("Employee details retrieved successfully")
    return db_emp


#----------depends-----------

@employees.get("/get_id_by_token_depends",response_model=EmployeeAll)
def get_id_by_token(emp_id=Depends(decode_token_emp_id)):
    db_emp = db.query(employee).filter(employee.id == emp_id, employee.is_active == True).first()
    if db_emp is None:
        raise HTTPException (status_code=404,detail="emp not found")
    return db_emp

#------------header---------------

@employees.get("/get_id_by_token_header",response_model=EmployeeAll)
def get_id_by_token_header(token=Header(...)):
    emp_id = decode_token_emp_id(token)
    db_emp = db.query(employee).filter(employee.id == emp_id, employee.is_active == True).first()
    if db_emp is None:
        raise HTTPException (status_code=404,detail="emp not found")
    return db_emp

#-------------------------get all emp--------------------------

@employees.get("/get_all_emp",response_model=list[EmployeeAll])
def get_all_emp():
    logger.info("Attempting to retrieve all employee information.")
    db_emp = db.query(employee).all()
    logger.success("employee retrieved succesfully")
    if db_emp is None:
        logger.info("employee not found")
        raise HTTPException(status_code=404,detail="emp not found")
    
    logger.success("Employee information retrieved successfully")
    return db_emp

#-------------------------update by token----------------------------

@employees.put("/update_emp_by_token",response_model=EmployeeAll)
def update_emp_token(token : str , emp : EmployeeAll):
    logger.info("access update employee details using token.")
    emp_id = decode_token_emp_id(token)
    logger.info("Decoded employee ID from token")
    
    db_emp = db.query(employee).filter(employee.id == emp_id , employee.is_active == True).first()
    logger.info("retrieving employee data from database")
    
    if db_emp is None:
        logger.error("Employee not found.")
        raise HTTPException (status_code=404,detail="emp not found")
    
    logger.info("Updating employee details for employee ID")
    
    db_emp.emp_name = emp.emp_name,
    db_emp.email = emp.email,
    db_emp.phone_no = emp.phone_no,
    db_emp.position = emp.position,
    db_emp.password = pwd_context.hash(emp.password)
    
    db.commit()
    logger.success("Employee details updated successfully for employee ID")
    return db_emp

#-----------depends-------------

@employees.put("/update_emp_by_token_depends",response_model=EmployeeAll)
def update_emp_token_depends( emp : EmployeeAll,emp_id=Depends(decode_token_emp_id)):
    db_emp = db.query(employee).filter(employee.id == emp_id , employee.is_active == True).first()
    if db_emp is None:
        raise HTTPException (status_code=404,detail="emp not found")
    
    db_emp.emp_name = emp.emp_name,
    db_emp.email = emp.email,
    db_emp.phone_no = emp.phone_no,
    db_emp.position = emp.position,
    db_emp.password = pwd_context.hash(emp.password)
    
    db.commit()
    return db_emp

#----------header-----------

@employees.put("/update_emp_by_token_header",response_model=EmployeeAll)
def update_emp_token_header( emp : EmployeeAll,token=Header(...)):
    emp_id = decode_token_emp_id(token)
    db_emp = db.query(employee).filter(employee.id == emp_id , employee.is_active == True).first()
    if db_emp is None:
        raise HTTPException (status_code=404,detail="emp not found")
    
    db_emp.emp_name = emp.emp_name,
    db_emp.email = emp.email,
    db_emp.phone_no = emp.phone_no,
    db_emp.position = emp.position,
    db_emp.password = pwd_context.hash(emp.password)
    
    db.commit()
    return db_emp
    
#----------------------------delete by token-----------------------------

@employees.delete("/delete_emp_by_token")
def delete_emp_token(token:str):
    logger.info("accessing employee details using token")
    
    emp_id = decode_token_emp_id(token)
    logger.info("Decoded employee ID from token")
    
    db_emp = db.query(employee).filter(employee.id == emp_id, employee.is_active == True).first()
    logger.info("retrieving employee data from database")
    
    if db_emp is None :
        logger.error("employee not found")
        raise HTTPException (status_code=404,detail="emp not found")
    
    db_emp.is_active = False
    db_emp.is_delete = True
    
    db.commit()
    logger.success("Employee details deleted successfully for employee ID")
    return {"Employee Delete successfully"}   

#--------depends----------

@employees.delete("/delete_emp_by_token_depends")
def delete_emp_token_depends(emp_id=Depends(decode_token_emp_id)):
    db_emp = db.query(employee).filter(employee.id == emp_id, employee.is_active == True).first()
    if db_emp is None :
        raise HTTPException (status_code=404,detail="emp not found")
    
    db_emp.is_active = False
    db_emp.is_delete = True
    
    db.commit()
    return {"Employee Delete successfully"}   

#-----------header------------

@employees.delete("/delete_emp_by_token_header")
def delete_emp_token_header(token=Header(...)):
    emp_id = decode_token_emp_id(token)
    db_emp = db.query(employee).filter(employee.id == emp_id, employee.is_active == True).first()
    if db_emp is None :
        raise HTTPException (status_code=404,detail="emp not found")
    
    db_emp.is_active = False
    db_emp.is_delete = True
    
    db.commit()
    return {"Employee Delete successfully"}   


#------------------------------Reregister by token -----------------------------

@employees.put("/reregister_emp")
def reregister_emp(token : str,emp : EmpPass):
     logger.info("Attempting to reregister employee using token")
     
     emp_id = decode_token_emp_id(token)
     logger.info("Decoded employee ID from token")
     
     db_emp = db.query(employee).filter(employee.id == emp_id).first()
     logger.info("Checking if employee exists in the database")
     
     if db_emp is None :
         logger.error("Employee not found")
         raise HTTPException (status_code=404,detail="emp not found")
     
     if db_emp.is_delete is True and db_emp.is_active is False:
         logger.info("Employee is marked as deleted and inactive")
         if pwd_context.verify(emp.password,db_emp.password):
             logger.info("Password verification successful")
             
             db_emp.is_delete = False
             db_emp.is_active = True
             
             db.commit()
             logger.info("Employee reregistered successfully for employee ID")
             return True
         
     logger.error("Invalid credentials provided")   
     raise HTTPException(status_code=404,detail="Invalid credentials")
 
 #---------depends--------
 
@employees.put("/reregister_emp_depends")
def reregister_emp_depends(emp : EmpPass,emp_id=Depends(decode_token_emp_id)):
     db_emp = db.query(employee).filter(employee.id == emp_id).first()
     if db_emp is None :
         raise HTTPException (status_code=404,detail="emp not found")
     
     if db_emp.is_delete is True and db_emp.is_active is False:
         if pwd_context.verify(emp.password,db_emp.password):
             
             db_emp.is_delete = False
             db_emp.is_active = True
             
             db.commit()
             return True
         
     raise HTTPException(status_code=404,detail="Invalid credentials")
 
#-----------header----------------

@employees.put("/reregister_emp_header")
def reregister_emp_header(emp : EmpPass,token=Header(...)):
     emp_id = decode_token_emp_id(token)
     db_emp = db.query(employee).filter(employee.id == emp_id).first()
     if db_emp is None :
         raise HTTPException (status_code=404,detail="emp not found")
     
     if db_emp.is_delete is True and db_emp.is_active is False:
         if pwd_context.verify(emp.password,db_emp.password):
             
             db_emp.is_delete = False
             db_emp.is_active = True
             
             db.commit()
             return True
         
     raise HTTPException(status_code=404,detail="Invalid credentials")

#-----------------------------Forget password token------------------------------- 

@employees.put("/forget_password_by_token")
def forget_password_token(token : str , newpass : str):
    logger.info("Attempting to reset password using token")
    
    emp_id = decode_token_emp_id(token)
    logger.info("Decoded employee ID from token")
    
    db_emp = db.query(employee).filter(employee.id == emp_id).first()
    logger.info("Checking if employee exists in the database")
    
    if db_emp is None :
        logger.error("Employee not found")
        raise HTTPException(status_code=404,detail="emp not found")
    
    logger.info("Resetting password for employee ID")
    db_emp.password = pwd_context.hash(newpass)
    
    db.commit()
    logger.success("Password reset successfully for employee ID")
    return {"Forget password successfully"}

#------------depends--------------

@employees.put("/forget_password_by_token_depends")
def forget_password_token_depends( newpass : str,emp_id=Depends(decode_token_emp_id)):
    db_emp = db.query(employee).filter(employee.id == emp_id).first()
    if db_emp is None :
        raise HTTPException(status_code=404,detail="emp not found")
    
    db_emp.password = pwd_context.hash(newpass)
    
    db.commit()
    return {"Forget password successfully"}

#----------header-----------

@employees.put("/forget_password_by_token_header")
def forget_password_token_header(newpass : str,token=Header(...)):
    emp_id = decode_token_emp_id(token)
    db_emp = db.query(employee).filter(employee.id == emp_id).first()
    if db_emp is None :
        raise HTTPException(status_code=404,detail="emp not found")
    
    db_emp.password = pwd_context.hash(newpass)
    
    db.commit()
    return {"Forget password successfully"}

#-----------------------------Reset passowrd token----------------------------

@employees.put("/reset_password_by_token")
def reset_password_by_token(token : str , oldpass : str , newpass : str):
    logger.info("Attempting to reset password using token")
    
    emp_id = decode_token_emp_id(token)
    logger.info("Decoded employee ID from token")
    
    db_emp = db.query(employee).filter(employee.id == emp_id).first()
    logger.info("Checking if employee exists in the database")
    
    if db_emp is None :
        logger.error("Employee not found")
        raise HTTPException(status_code=404,detail="emp not found")
    
    logger.info("Verifying old password for employee ID")
    if pwd_context.verify(oldpass , db_emp.password):
        logger.info("Old password verified, updating to new password")
        
        db_emp.password = pwd_context.hash(newpass)
        
        db.commit()
        logger.success("Password reset successfully for employee ID")
        return "password reset successfully"
    else:
        logger.error("Old password not matched for employee ID")
        return "old password not matched"
    
#----------depends-----------


@employees.put("/reset_password_by_token_depends")
def reset_password_by_token_depends(token : str , oldpass : str , newpass : str):
    emp_id = decode_token_emp_id(token)
    db_emp = db.query(employee).filter(employee.id == emp_id).first()
    if db_emp is None :
        raise HTTPException(status_code=404,detail="emp not found")
    
    if pwd_context.verify(oldpass , db_emp.password):
        db_emp.password = pwd_context.hash(newpass)
        db.commit()
        return "password reset successfully"
    else:
        return "old password not matched"
    
#------------header------------


@employees.put("/reset_password_by_token_header")
def reset_password_by_token_header( oldpass : str , newpass : str,token=Header(...)):
    emp_id = decode_token_emp_id(token)
    db_emp = db.query(employee).filter(employee.id == emp_id).first()
    if db_emp is None :
        raise HTTPException(status_code=404,detail="emp not found")
    
    if pwd_context.verify(oldpass , db_emp.password):
        db_emp.password = pwd_context.hash(newpass)
        db.commit()
        return "password reset successfully"
    else:
        return "old password not matched"

#--------------------------login encode token ---------------------------------

@employees.get("/encode_token_login")
def encode_token_login(emp_name : str ,password : str):
    logger.info("Generating access token for login")
    
    access_token = get_token_login(emp_name,password)
    logger.success("Access token generated successfully")
    
    return access_token

#-------------------------login token------------------------------
    
@employees.get("/login_token")  
def login_token(token : str ):
    logger.info("Attempting to log in using token")
    
    emp_name = decode_token_emp_name(token)  
    logger.info("Decoded employee name from token")
    
    password = decode_token_password(token)
    logger.info("Decoded password from token")
    
    db_emp = db.query(employee).filter(employee.emp_name == emp_name,employee.is_active==True).first()
    logger.info("Querying database for employee details")
    
    if db_emp is None:
        logger.error("Employee not found")
        raise HTTPException(status_code=404,detail="emp not found")
    
    if not pwd_context.verify(password,db_emp.password):
        logger.error("Incorrect password")
        raise HTTPException(status_code=401,detail="incorrect password")
    
    logger.success("Login successful")
    return "login successfully"
    
    
#----------depends---------

@employees.get("/login_token_depends")  
def login_token_depends(emp_name=Depends(decode_token_emp_name) ,password=Depends(decode_token_password)):
    db_emp = db.query(employee).filter(employee.emp_name == emp_name,employee.is_active==True).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail="emp not found")
    
    if not pwd_context.verify(password,db_emp.password):
        raise HTTPException(status_code=401,detail="incorrect password")
    
    return "login successfully"

#-----------header------------

@employees.get("/login_token_header")  
def login_token_header(token=Header(...) ):
    emp_name = decode_token_emp_name(token)  
    password = decode_token_password(token)
    db_emp = db.query(employee).filter(employee.emp_name == emp_name,employee.is_active==True).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail="emp not found")
    
    if not pwd_context.verify(password,db_emp.password):
        raise HTTPException(status_code=401,detail="incorrect password")
    
    return "login successfully"
    
#------------------------------------------------------------------------------


@employees.patch("/update_emp/{emp_id}", response_model=EmployeeAll)
def update_emp_by_id(emp_id: str, emp_update: dict):
    db_emp = db.query(employee).filter(employee.id == emp_id, employee.is_active == True).first()
    
    if db_emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Update only the fields provided in the emp_update dictionary
    if "emp_name" in emp_update:
        db_emp.emp_name = emp_update["emp_name"]
    if "email" in emp_update:
        db_emp.email = emp_update["email"]
    if "phone_no" in emp_update:
        db_emp.phone_no = emp_update["phone_no"]
    if "position" in emp_update:
        db_emp.position = emp_update["position"]
    if "password" in emp_update:
        db_emp.password = pwd_context.hash(emp_update["password"])
    
    db.commit()
    return db_emp
    
    
    
    
    

       
            