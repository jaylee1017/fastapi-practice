from database.repository import UserRepository
from fastapi import APIRouter, Depends, HTTPException
from schema.request import SignUpRequest, LogInRequest
from schema.response import UserSchema, JWTResponse
from service.user import UserService
from database.orm import User

router = APIRouter(prefix="/users")

@router.post("/sign-up", status_code=201) # 생성은 코드 201
def user_sign_up_handler(
        request: SignUpRequest,
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends(UserRepository),
):
    # 1. request body(username, password)
    # 2. password -> hashing -> 암호화 -> hashed_password
    hashed_password: str = user_service.hash_password(
        plain_password=request.password)
    # 3. User(username, hashed_password)
    user: User = User.create(
        username=request.username, hashed_password=hashed_password)

    # 이때까지는 user가 그냥 orm 객체로 존재함
    # 4. user -> db save (레포지터리 패턴 사용) 이때부터 실제로 저장됨
    user: user = user_repo.save_user(user=user) # id = int
    # 5. return user(id, username)
    return UserSchema.from_orm(user)


@router.post("/log-in")
def user_log_in_handler(
        request: LogInRequest,
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends(UserRepository),
):
    # 1. request body(username, password)
    # 2. db read user
    user: User | None = user_repo.get_user_by_username(
        username=request.username)
    if not User:
        raise HTTPException(status_code=404, detail="User Not Found")
    # 3. user.password(hashed), request.password(plain) -> bcrypt.checkpw
    verified: bool = user_service.verify_password(
        plain_password=request.password,
        hashed_password=user.password
    )
    if not verified:
        raise HTTPException(status_code=401, detail="Not Authorized")
    # 4. create jwt
    access_token: str = user_service.create_jwt(username=user.username)

    # 5. return jwt
    return JWTResponse(access_token=access_token)