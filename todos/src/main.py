from typing import List

from database.orm import ToDo
from database.repository import get_todos, get_todo_by_todo_id, create_todo, update_todo, delete_todo
from fastapi import FastAPI, Body, HTTPException,Depends
from schema.request import CreateToDoRequest
from schema.response import ToDoListSchema, ToDoSchema
from sqlalchemy.orm import Session

from database.connection import get_db

app = FastAPI()


# 안에서 type 유효성 검사등을 거침


@app.get("/")
def health_check_handler():
    return {"ping": "pong"}


todo_data = {
    1: {
        "id": 1,
        "contents": "실전! FastAPI 섹션 0 수강",
        "is_done": True,
    },
    2: {
        "id": 2,
        "contents": "실전! FastAPI 섹션 1 수강",
        "is_done": False,
    },
    3: {
        "id": 3,
        "contents": "실전! FastAPI 섹션 2 수강",
        "is_done": False,
    }
}


# 쿼리 파라미터 > 함수의 인자로 전달 > Swagger에서 사용자 입력받음
# order 순서를 지정하거나, 특정 값을 가진 데이터만을 조회 가능

@app.get("/todos", status_code=200) #status_code 따로 적지 않으면 200이 기본값
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


@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(todo_id: int,
                     session: Session = Depends(get_db),
                     ) -> ToDoSchema:
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="ToDo Not Found")


@app.post("/todos", status_code=201)
def create_todo_handler(request: CreateToDoRequest,
                        session: Session = Depends(get_db),
                        ) -> ToDoSchema:
    todo: ToDo = ToDo.create(request=request) # todo의 id = None
    todo: ToDo = create_todo(session=session, todo=todo) # todo의 id에 int값 들어감
    return ToDoSchema.from_orm(todo)
# pydantic으로 들어온 데이터를 orm 으로 바꿔 저장해야돼(get과 반대)

@app.patch("/todos/{todo_id}", status_code=200)
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

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(todo_id: int,
                        session: Session = Depends(get_db)
                        ):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo Not Found")

    delete_todo(session=session, todo_id=todo_id)
# body가 비어서 리턴됨 (only header만 리턴됨)

''' docker run -p 3306:3306 -e MYSQL_ROOT_PASSWORD=todos -e MYSQL_DATABASE=todos -d -v todos:/db --name todos mysql:8.0
docker ps
docker logs todos
docker volume ls
 

MySQL 접속
docker exec -it todos bash  > bash에 접속
mysql -u root -p
 

SQL
SHOW databases;
USE todos;
CREATE TABLE todo(
    id INT NOT NULL AUTO_INCREMENT,
    contents VARCHAR(256) NOT NULL,
    is_done BOOLEAN NOT NULL,
    PRIMARY KEY (id)
);
INSERT INTO todo (contents, is_done) VALUES ("FastAPI Section 0", true);
SELECT * FROM todo;'''


