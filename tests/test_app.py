import pytest

import app as app_module


@pytest.fixture
def client():
    app_module.tasks.clear()
    app_module.next_id = 1
    app_module.app.testing = True
    with app_module.app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_list_starts_empty(client):
    assert client.get("/tasks").get_json() == []


def test_create_task(client):
    response = client.post("/tasks", json={"title": "Estudar DevOps"})
    assert response.status_code == 201
    assert response.get_json() == {"id": 1, "title": "Estudar DevOps", "done": False}


def test_create_task_without_title(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 400


def test_complete_task(client):
    client.post("/tasks", json={"title": "Configurar CI"})
    response = client.put("/tasks/1")
    assert response.status_code == 200
    assert response.get_json()["done"] is True


def test_complete_missing_task(client):
    assert client.put("/tasks/99").status_code == 404


def test_delete_task(client):
    client.post("/tasks", json={"title": "Escrever Terraform"})
    assert client.delete("/tasks/1").status_code == 204
    assert client.get("/tasks").get_json() == []


def test_delete_missing_task(client):
    assert client.delete("/tasks/99").status_code == 404
