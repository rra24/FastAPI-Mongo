from fastapi import FastAPI;
# from routes import router;
from app.studentRecordManager.routes.routes import studentApp ;
from app.administratorStaff.admin_staff import app_admin;
from app.accessAuthentication.access_authentication import app_access;
from app.programModules.programModules import app_program;

app = FastAPI()

# app.include_router(router);
app.include_router(
    app_access, 
    tags=["Login and Authentication"]
);

app.include_router(
    studentApp,
    tags=["Student Record Manager"]
);
app.include_router(
    app_admin,
    tags=["Administrative staff Manager"]
);

app.include_router(
    app_program,
    tags=["Program and Module Manager"]
);



# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi

# uri = "mongodb+srv://admin:Abcd@cluster0.2cjvxnm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)