from fastapi import FastAPI,HTTPException,APIRouter
from database.database import SessionLocal
from src.models.student_details import Stu
from src.schemas.student import Student,StuBase
import uuid



studentde = APIRouter()

db = SessionLocal()

@studentde.post("/student_detail_create/",response_model=Student)
def Create_student_detail(stu: Student):
    newstudent = Stu(
        f_name = stu.f_name,
        m_name = stu.m_name,
        l_name = stu.l_name,
        roll_no = stu.roll_no,
        age = stu.age,
        email = stu.email,
        phone_no = stu.phone_no,
        address = stu.address,
        branch = stu.branch,
        dob = stu.dob,
        admission_date = stu.admission_date,
        gender = stu.gender,
        adharcard_no = stu.adharcard_no,
        cast = stu.cast,
        state = stu.state,
        fees = stu.fees,
        hsc_percentage = stu.hsc_percentage,
    )
    db.add(newstudent)
    db.commit()
    return newstudent


@studentde.get("/student_detail_student/{student_id}",response_model=StuBase)
def read_student_detail(student_id:str=str(uuid.uuid4())):
    stu = db.query(Stu).filter(Stu.id == student_id).first()
    if stu is  None:
        raise HTTPException(status_code=404,detail="student not found")
    return stu

@studentde.get("/student_detail_roll_no/{student_roll_no}",response_model=StuBase)
def read_student_roll_non(student_roll_no:str):
    stu = db.query(Stu).filter(Stu.roll_no == student_roll_no).first()
    breakpoint()
    if stu is  None:
        raise HTTPException(status_code=404,detail="student not found")
    return stu

@studentde.get("/student_all_detail/", response_model=list[Student])
def read_student_list():
    stu = db.query(Stu).all()
    length_list = len(stu)
    if length_list == 0:
        raise HTTPException(status_code=404, detail="Table is empty")
    return stu

@studentde.put("/student_detail_update/{student_id}",response_model=Student)
def update_student(student_id:str,stu1 : Student):
    db_stu = db.query(Stu).filter(Stu.id == student_id).first()
    if db_stu is None:
        raise HTTPException(status_code=404,detail="Student not found")

    db_stu.f_name = stu1.f_name,
    db_stu.m_name = stu1.m_name,
    db_stu.l_name = stu1.l_name,
    db_stu.roll_no = stu1.roll_no,
    db_stu.phone_no = stu1.phone_no,
    db_stu.gender = stu1.gender,
    db_stu.branch = stu1.branch,
    db_stu.age = stu1.age,
    db_stu.email = stu1.email,
    db_stu.address = stu1.address,
    db_stu.dob = stu1.dob,
    db_stu.admission_date = stu1.admission_date,
    db_stu.adharcard_no = stu1.adharcard_no
    db_stu.cast = stu1.cast,
    db_stu.state = stu1.state,
    db_stu.fees = stu1.fees,
    db_stu.hsc_percentage = stu1.hsc_percentage 
    
    db.commit()
    return db_stu

@studentde.delete("/student_detail_delete/{student_id}")
def delete_student(student_id:str):
    db_student = db.query(Stu).filter(Stu.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404,detail="student not found")
    
    db.delete(db_student)
    db.commit()
    return {"message":"student deleted successfully"}