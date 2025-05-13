from typing import List

from database.connection import get_db
from database.orm import ToDo
from database.repository import get_todos, get_todo_by_todo_id, create_todo, update_todo, delete_todo
from fastapi import Depends, HTTPException, Body, APIRouter # APIRouter : main.py와 라우팅하기위해 import 필요함
# from main import app
from schema.request import CreateToDoRequest
from schema.response import ToDoListSchema, ToDoSchema
from sqlalchemy.orm import Session

router = APIRouter()

# ctrl + D = select same words all at once
# for routing, app을 router로 바꾼다
@router.get("/todos", status_code=200) #status_code 따로 적지 않으면 200이 기본값
def get_todos_handler(
        order: str | None = None,
        session: Session = Depends(get_db),
) -> ToDoListSchema:
    todos: List[ToDo] = get_todos(session=session)
   # ret = list(todo_data.values())
    if order and order == "DESC":  # order가 존재하고, order가 DESC
        return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos[::-1]]
    )
    return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos]
    )


@router.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(todo_id: int,
                     session: Session = Depends(get_db),
                     ) -> ToDoSchema:
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="ToDo Not Found")


@router.post("/todos", status_code=201)
def create_todo_handler(request: CreateToDoRequest,
                        session: Session = Depends(get_db),
                        ) -> ToDoSchema:
    todo: ToDo = ToDo.create(request=request) # todo의 id = None
    todo: ToDo = create_todo(session=session, todo=todo) # todo의 id에 int값 들어감
    return ToDoSchema.from_orm(todo)


@router.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(..., embed=True),
        session: Session = Depends(get_db),
):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        todo.done() if is_done else todo.undone()
        todo: ToDo = update_todo(session=session, todo=todo)
        # update
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="ToDo Not Found")


@router.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(todo_id: int,
                        session: Session = Depends(get_db)
                        ):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo Not Found")
    delete_todo(session=session, todo_id=todo_id)
