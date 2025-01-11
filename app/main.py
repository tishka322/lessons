from fastapi import FastAPI
from app.routers import task, user
import app.models.user as user_model
import app.models.task as task_model

app = FastAPI()

app.include_router(task.router)
app.include_router(user.router)


@app.get('/')
async def welcome():
    return {"message": "Welcome to Taskmanager"}
