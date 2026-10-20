from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from . import crud, database, models, schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Student Database CRUD API",
    description="A FastAPI application for managing student records with CRUD operations",
    version="1.1.0",
)


@app.get("/")
def root():
    return {"message": "Student Database CRUD API"}


@app.post("/students", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: schemas.StudentCreate, db: Session = Depends(database.get_db)):
    if crud.get_student_by_email(db, email=student.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    return crud.create_student(db=db, student=student)


@app.get("/students", response_model=List[schemas.StudentResponse])
def read_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    name: Optional[str] = None,
    course: Optional[str] = None,
    email: Optional[str] = None,
    db: Session = Depends(database.get_db),
):
    return crud.get_students(db, skip=skip, limit=limit, name=name, course=course, email=email)


@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def read_student(student_id: int, db: Session = Depends(database.get_db)):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@app.put("/students/{student_id}", response_model=schemas.StudentResponse)
@app.patch("/students/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(database.get_db)):
    if student.email:
        existing = crud.get_student_by_email(db, email=student.email)
        if existing and existing.id != student_id:
            raise HTTPException(status_code=409, detail="Email already registered")
    db_student = crud.update_student(db=db, student_id=student_id, student=student)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@app.delete("/students/{student_id}", response_model=schemas.StudentResponse)
def delete_student(student_id: int, db: Session = Depends(database.get_db)):
    db_student = crud.delete_student(db=db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student
