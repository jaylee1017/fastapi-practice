from typing import List

from pydantic import BaseModel

class ToDoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool

    class Config:
        orm_mode = True
        # pydanticdml Config 클래스에서 orm_mode = True를 하면 from_orm 사용 가능
        # from_orm : orm객체를 스키마로 변경 (db에서 가져온 orm객체는 그 자체로 JSON으로 응답 불가)


# in 윈도우 : ctrl + 클릭 -> 클래스가 정의된 곳으로 자동 이동...
class ToDoListSchema(BaseModel):
    todos: List[ToDoSchema]
    # 리팩터링 기능 -> 자동으로 이름 모두 변경.. 등의 기능!


class UserSchema(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True