from fastapi import FastAPI, HTTPException, status , APIRouter
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List, Optional

app_admin = APIRouter()

# MongoDB setup
client = MongoClient("mongodb+srv://admin:Abcd@cluster0.2cjvxnm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["corporate_management"]
staff_collection = db["administrative_staff"]

class StaffMember(BaseModel):
    staff_id: int
    name: str
    email: str
    role: str
    permissions: List[str]  # Permissions are simplified as a list of strings

class StaffUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    permissions: Optional[List[str]] = None

@app_admin.post("/staff/", response_model=StaffMember, status_code=status.HTTP_201_CREATED)
def create_staff_member(staff_member: StaffMember):
    if staff_collection.find_one({"staff_id": staff_member.staff_id}):
        raise HTTPException(status_code=400, detail="Staff member already exists")
    staff_collection.insert_one(staff_member.dict())
    return staff_member

@app_admin.get("/staff/{staff_id}", response_model=StaffMember)
def get_staff_member(staff_id: int):
    staff = staff_collection.find_one({"staff_id": staff_id})
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return staff

@app_admin.put("/staff/{staff_id}", response_model=StaffMember)
def update_staff_member(staff_id: int, staff_update: StaffUpdate):
    updated_data = {k: v for k, v in staff_update.dict(exclude_unset=True).items()}
    result = staff_collection.update_one({"staff_id": staff_id}, {"$set": updated_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return staff_collection.find_one({"staff_id": staff_id})

@app_admin.delete("/staff/{staff_id}")
def delete_staff_member(staff_id: int):
    result = staff_collection.delete_one({"staff_id": staff_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return {"message": "Staff member deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app_admin, host="127.0.0.1", port=8000)