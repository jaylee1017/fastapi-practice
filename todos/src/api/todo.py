from typing import List

from database.connection import get_db
from database.orm import ToDo
from database.repository import ToDoRepository
from fastapi import Depends, HTTPException, Body, APIRouter # APIRouter : main.py와 라우팅하기위해 import 필요함
# from main import app
from schema.request import CreateToDoRequest
from schema.response import ToDoListSchema, ToDoSchema
from sqlalchemy.orm import Session

router = APIRouter(prefix="/todos")
# prefix : 반복되는 부분 제거

# ctrl + D = select same words all at once
# for routing, app을 router로 바꾼다
@router.get("", status_code=200) #status_code 따로 적지 않으면 200이 기본값
def get_todos_handler(
        order: str | None = None,
        todo_repo: ToDoRepository = Depends(ToDoRepository),
) -> ToDoListSchema:
    todos: List[ToDo] = todo_repo.get_todos()
   # ret = list(todo_data.values())
    if order and order == "DESC":  # order가 존재하고, order가 DESC
        return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos[::-1]]
    )
    return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos]
    )


@router.get("/{todo_id}", status_code=200)
def get_todo_handler(todo_id: int,
                     todo_repo: ToDoRepository = Depends(ToDoRepository),
                     ) -> ToDoSchema:
    todo: ToDo | None = todo_repo.get_todo_by_todo_id(todo_id=todo_id)
    if todo:
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="ToDo Not Found")


@router.post("", status_code=201)
def create_todo_handler(request: CreateToDoRequest,
                        todo_repo: ToDoRepository = Depends(ToDoRepository),
                        ) -> ToDoSchema:
    todo: ToDo = ToDo.create(request=request) # todo의 id = None
    todo: ToDo = todo_repo.create_todo(todo=todo) # todo의 id에 int값 들어감
    return ToDoSchema.from_orm(todo)


@router.patch("/{todo_id}", status_code=200)
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(..., embed=True),
        todo_repo: ToDoRepository = Depends(ToDoRepository),
):
    todo: ToDo | None = todo_repo.get_todo_by_todo_id(todo_id=todo_id)
    if todo:
        todo.done() if is_done else todo.undone()
        todo: ToDo = todo_repo.update_todo(todo=todo)
        # update
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="ToDo Not Found")


@router.delete("/{todo_id}", status_code=204)
def delete_todo_handler(todo_id: int,
                        todo_repo: ToDoRepository = Depends(ToDoRepository),
                        ):
    todo: ToDo | None = todo_repo.get_todo_by_todo_id(todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo Not Found")
    todo_repo.delete_todo(todo_id=todo_id)
