'''
fixtureの定義ファイル
fixture: テストの前処理(DBセットアップ、モック作成など)のためのpytestの機能
'''
import os
import sys

app_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(app_dir)# sys.pathは、Pythonがモジュール検索時に使用するパスのリスト(mainをimportするために必要)


import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from main import app
from models import Base, Todo
from schemas import DecodedToken
from database import get_db
from cruds.auth import get_current_user


# 擬似セッションの設定
@pytest.fixture()
def session_fixture():
    # 擬似セッションの生成
    engine = create_engine(
        url="sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
    db = SessionLocal()

    try:
        # 初期データの設定
        todo1 = Todo(title="clean room", user_id=1)
        todo2 = Todo(title="make dinner", user_id=1)
        db.add(todo1)
        db.add(todo2)
        db.commit()
        yield db
    finally:
        db.close()


# テスト中に使用する擬似ユーザー情報(モック)の設定
@pytest.fixture()
def user_fixture():
    return DecodedToken(username="user1", user_id=1)


@pytest.fixture()
def client_fixture(session_fixture: Session, user_fixture: DecodedToken):
    def override_get_db():
        return session_fixture
    
    def override_get_current_user():
        return user_fixture
    
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()