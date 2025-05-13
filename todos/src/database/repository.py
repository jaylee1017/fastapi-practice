from typing import List

from database.connection import get_db
from fastapi import Depends
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database.orm import ToDo, User


class ToDoRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session
# 전체 조회 함수
    def get_todos(self) -> List[ToDo]:
        return list(self.session.scalars((select(ToDo))))

# 단일 조회 함수       ToDo 또는 None을 리턴함
    def get_todo_by_todo_id(self, todo_id: int) -> ToDo | None:
        return self.session.scalar(select(ToDo).where(ToDo.id == todo_id))
    # ToDo가 존재하면 ToDo를 리턴, 그렇지 않으면 None을 리턴함

    # scalar(), scalars() : db 쿼리 결과를 추출할 때 사용하는 함수
    # 리턴값은 대부분 ORM 객체나 그 객체의 속성값

    def create_todo(self, todo: ToDo) -> ToDo:
        self.session.add(instance=todo)
        self.session.commit() # db save
        self.session.refresh(instance=todo) # db read -> todo_id 결정
        return todo

    def update_todo(self, todo: ToDo) -> ToDo:
        self.session.add(instance=todo)
        self.session.commit()  # db save
        self.session.refresh(instance=todo)  # db read -> todo_id 결정
        return todo

    def delete_todo(self, todo_id: int) -> None:
        self.session.execute(delete(ToDo).where(ToDo.id == todo_id))
        self.session.commit()



class UserRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def save_user(self, user: User) -> User:
        self.session.add(instance=user)
        self.session.commit()
        self.session.refresh(instance=user)
        return user





