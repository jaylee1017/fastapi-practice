from fastapi import FastAPI

from api import todo, user

app = FastAPI()
app.include_router(todo.router)
app.include_router(user.router)

# httpx == 0.27.2

# 안에서 type 유효성 검사등을 거침


@app.get("/")
def health_check_handler():
    return {"ping": "pong"}


# 쿼리 파라미터 > 함수의 인자로 전달 > Swagger에서 사용자 입력받음
# order 순서를 지정하거나, 특정 값을 가진 데이터만을 조회 가능


# pydantic으로 들어온 데이터를 orm 으로 바꿔 저장해야돼(get과 반대)


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


