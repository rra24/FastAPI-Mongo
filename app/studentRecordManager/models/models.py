from pydantic import BaseModel

class StudentRecord(BaseModel):
    studentName:str
    studentId:str
    studenEmail:str