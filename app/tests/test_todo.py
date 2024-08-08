from fastapi.testclient import TestClient


# READテスト
def test_get_all_todos(client_fixture: TestClient):
    response = client_fixture.get("/todos")
    assert response.status_code == 200

    todos = response.json()
    assert len(todos) == 2

def test_get_todo_by_id_正常系(client_fixture: TestClient):
    response = client_fixture.get("/todos/1")
    assert response.status_code == 200

    todo = response.json()
    assert todo["id"] == 1

def test_get_todo_by_id_異常系(client_fixture: TestClient):
    response = client_fixture.get("/todos/10")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


# CREATEのテスト
def test_create_todo(client_fixture: TestClient):
    response = client_fixture.post(
        "/todos",
        json={"title": "running", "user_id": 1}
    )
    assert response.status_code == 201

    todo = response.json()
    assert todo["title"] == "running"
    assert todo["id"] == 3

    response = client_fixture.get("/todos")
    assert len(response.json()) == 3


# UPDATEのテスト
def test_update_todo_正常系(client_fixture: TestClient):
    response = client_fixture.patch(
        "/todos/1",
        json={"status": "COMPLETED"}
    )
    assert response.status_code == 200

    todo = response.json()
    assert todo["status"] == "COMPLETED"

def test_update_todo_異常系(client_fixture: TestClient):
    response = client_fixture.patch(
        "/todos/10",
        json={"status": "COMPLETED"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not updated"


# DELETEのテスト
def test_delete_todo_正常系(client_fixture: TestClient):
    response = client_fixture.delete("/todos/1")
    assert response.status_code == 200

    response = client_fixture.get("/todos")
    assert len(response.json()) == 1

def test_delete_todo_異常系(client_fixture: TestClient):
    response = client_fixture.delete("/todos/10")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not deleted"

    response = client_fixture.get("/todos")
    assert len(response.json()) == 2