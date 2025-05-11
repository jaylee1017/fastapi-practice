import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app=app)
# @pytest.fixture 데코레이터 -> client를 tests 디렉 내에서 공유 사용 가능