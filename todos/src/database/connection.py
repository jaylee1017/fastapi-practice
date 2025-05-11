from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:todos@127.0.0.1:3306/todos"


engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
# echo 옵션 : 어떤 쿼리가 나가고 있는지 출력 > 디버그 단계에서 사용
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 제너레이터 -> db 연동
def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()