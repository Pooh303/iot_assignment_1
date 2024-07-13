from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import models
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router_v1 = APIRouter(prefix='/api')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router_v1.get('/students')
async def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

@router_v1.get('/students/{student_id}')
async def get_student(student_id: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if not student:
        return {"detail": f"Student_ID {student_id} not found"}
    return student

@router_v1.post('/students')
async def create_student(student: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    student = models.Student(
        first_name=student['first_name'],
        last_name=student['last_name'],
        student_id=student['student_id'],
        birth_date=student['birth_date'],
        gender=student['gender']
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    response.status_code = 201
    return {"detail": f"Student added successfully"}

@router_v1.patch('/students/{student_id}')
async def update_student(student_id: str, student_data: dict, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if not student:
        return {"detail": "Student not found"}

    for key, value in student_data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return {"detail": f"StudentID {student_id} updated successfully"}

@router_v1.delete('/students/{student_id}')
async def delete_student(student_id: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if not student:
        return {"detail": "Student not found"}
    
    db.delete(student)
    db.commit()
    return {"detail": f"StudentID {student_id} deleted successfully"}

app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
