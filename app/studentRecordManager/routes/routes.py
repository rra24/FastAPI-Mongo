from fastapi import FastAPI, HTTPException, status , APIRouter
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List, Optional

studentApp = APIRouter();

# MongoDB setup
client = MongoClient("mongodb+srv://admin:Abcd@cluster0.2cjvxnm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["education_system"]
students_collection = db["students"]

class StudyPlan(BaseModel):
    course_id: int
    course_name: str
    semester: str
    year: int

class AcademicRecord(BaseModel):
    course_id: int
    grade: str

class StudentRecord(BaseModel):
    student_id: int
    name: str
    email: str
    study_plan: List[StudyPlan]
    academic_records: List[AcademicRecord]

@studentApp.post("/students/", status_code=status.HTTP_201_CREATED)
def create_student_record(student_record: StudentRecord):
    if students_collection.find_one({"student_id": student_record.student_id}):
        raise HTTPException(status_code=400, detail="Student record already exists")
    students_collection.insert_one(student_record.dict())
    return {"message": "Student record created successfully"}

@studentApp.get("/students/{student_id}")
def get_student_record(student_id: int):
    student = students_collection.find_one({"student_id": student_id}, {'_id': 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@studentApp.put("/students/{student_id}")
def update_student_record(student_id: int, student_record: StudentRecord):
    result = students_collection.update_one({"student_id": student_id}, {"$set": student_record.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student record not found")
    return {"message": "Student record updated successfully"}

@studentApp.delete("/students/{student_id}")
def delete_student_record(student_id: int):
    result = students_collection.delete_one({"student_id": student_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student record not found")
    return {"message": "Student record deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(studentApp, host="127.0.0.1", port=8000)