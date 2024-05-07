from fastapi import FastAPI, HTTPException, status , APIRouter
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List, Optional

app_program = APIRouter()

# MongoDB setup
client = MongoClient("mongodb+srv://admin:Abcd@cluster0.2cjvxnm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["educational_system"]
modules_collection = db["modules"]
programs_collection = db["programs"]

class TimeSlot(BaseModel):
    day_of_week: str
    start_time: str
    end_time: str

class Module(BaseModel):
    module_id: int
    name: str
    study_level: str
    credit_value: int
    compulsory_in_programs: List[int]  # List of program IDs where this module is compulsory
    timetable: List[TimeSlot]

class Program(BaseModel):
    program_id: int
    name: str
    department: str
    modules: List[int]  # List of module IDs included in this program

@app_program.post("/modules/", response_model=Module, status_code=status.HTTP_201_CREATED)
def create_module(module: Module):
    if modules_collection.find_one({"module_id": module.module_id}):
        raise HTTPException(status_code=400, detail="Module already exists")
    modules_collection.insert_one(module.dict())
    return module

@app_program.get("/modules/{module_id}", response_model=Module)
def get_module(module_id: int):
    module = modules_collection.find_one({"module_id": module_id})
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module

@app_program.put("/modules/{module_id}", response_model=Module)
def update_module(module_id: int, module: Module):
    result = modules_collection.replace_one({"module_id": module_id}, module.dict())
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Module not found")
    return module

@app_program.post("/programs/", response_model=Program, status_code=status.HTTP_201_CREATED)
def create_program(program: Program):
    if programs_collection.find_one({"program_id": program.program_id}):
        raise HTTPException(status_code=400, detail="Program already exists")
    programs_collection.insert_one(program.dict())
    return program

@app_program.get("/programs/{program_id}", response_model=Program)
def get_program(program_id: int):
    program = programs_collection.find_one({"program_id": program_id})
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    return program

@app_program.put("/programs/{program_id}", response_model=Program)
def update_program(program_id: int, program: Program):
    result = programs_collection.replace_one({"program_id": program_id}, program.dict())
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Program not found")
    return program

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app_program, host="127.0.0.1", port=8000)
