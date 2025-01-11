from fastapi import FastAPI
from app.routers import task, user


app = FastAPI()


@app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}


app.include_router(task.task_router)
app.include_router(user.user_router)

# Python -m uvicorn main:app
# Python -m uvicorn app.main:app
# cd..
