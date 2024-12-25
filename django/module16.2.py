from fastapi import FastAPI, Path
from typing import Annotated

app=FastAPI()

@app.get('/')
async def main_page() -> str:
    return f"Главная страница"

@app.get('/user/admin')
async def admin_id() -> str:
    return f"Вы вошли как администратор"

@app.get('/user/{user_id}')
async def id_user(user_id: Annotated[int, Path(ge=1, le=100, description="Enter User ID")]):
    return f"Вы вошли как пользователь № {user_id}"
@app.get('/user/{username}/{age}')
async def get_user(username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username")],
                   age: Annotated[int, Path(ge=18, le=120, description="Enter age")]):
    return f"Информация о пользователе. Имя: {username}, Возраст: {age}"