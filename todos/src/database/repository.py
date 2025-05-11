from typing import List

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database.orm import ToDo

# 전체 조회 함수
def get_todos(session: Session) -> List[ToDo]:
    return list(session.scalars((select(ToDo))))

# 단일 조회 함수       ToDo 또는 None을 리턴함
def get_todo_by_todo_id(session: Session, todo_id: int) -> ToDo | None:
    return session.scalar(select(ToDo).where(ToDo.id == todo_id))
# ToDo가 존재하면 ToDo를 리턴, 그렇지 않으면 None을 리턴함

# scalar(), scalars() : db 쿼리 결과를 추출할 때 사용하는 함수
# 리턴값은 대부분 ORM 객체나 그 객체의 속성값

def create_todo(session: Session, todo: ToDo) -> ToDo:
    session.add(instance=todo)
    session.commit() # db save
    session.refresh(instance=todo) # db read -> todo_id 결정
    return todo


def update_todo(session: Session, todo: ToDo) -> ToDo:
    session.add(instance=todo)
    session.commit()  # db save
    session.refresh(instance=todo)  # db read -> todo_id 결정
    return todo

def delete_todo(session: Session, todo_id: int) -> None:
    session.execute(delete(ToDo).where(ToDo.id == todo_id))
    session.commit()

