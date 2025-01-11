from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import User, Task
from app.schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/")
async def all_user(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@user_router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    try:
        user = db.scalars(select(User).where(User.id == user_id))
        return user
    except IndexError:
        raise HTTPException(status_code=404, detail='Message Not found')


@user_router.get("/user_id/tasks")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalars(select(User).where(User.id == user_id)).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User was not found')

    db.scalars(select(Task).where(Task.user_id == user_id))
    return {"user_id": user.id, "tasks": [task for task in user.tasks]}


@user_router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    db.execute(insert(User).values(username=create_user.username,
                                   firstname=create_user.firstname,
                                   lastname=create_user.lastname,
                                   age=create_user.age,
                                   slug=slugify(create_user.username)))
    db.commit()

    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@user_router.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: UpdateUser):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found')
    db.execute(update(User).where(User.id == user_id).values(firstname=update_user.firstname,
                                                             lastname=update_user.lastname,
                                                             age=update_user.age,
                                                             ))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@user_router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalars(select(User).where(User.id == user_id)).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User was not found')

    db.execute(delete(Task).where(Task.user_id == user_id))
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User was deleted successful!'}
