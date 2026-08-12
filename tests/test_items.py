from fastapi.testclient import TestClient


def test_post_item(client: TestClient):
    response = client.post("/items", json={"name": "Laptop", "price": 999.99})
    data = response.json()

    assert response.status_code == 201
    assert data["name"] == "Laptop"
    assert data["price"] == 999.99
    assert data["in_stock"] is True


def test_post_item_missing_name(client: TestClient):
    response = client.post("/items", json={"price": 149.99})
    assert response.status_code == 422


def test_post_item_missing_price(client: TestClient):
    response = client.post("/items", json={"name": "Book"})
    assert response.status_code == 422


def test_get_items(client: TestClient):
    client.post("/items", json={"name": "Mug", "price": 11.00})
    client.post("/items", json={"name": "Bamboo plant", "price": 49.99})

    response = client.get("/items")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2


def test_get_item_by_id(client: TestClient):
    post_response = client.post("/items", json={"name": "Pencil", "price": 0.45})
    created_id = post_response.json()["id"]

    get_response = client.get(f"/items/{created_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Pencil"
    assert get_response.json()["price"] == 0.45

    get_response_no_item = client.get("/items/99999")
    assert get_response_no_item.status_code == 404


def test_restock_item(client: TestClient):
    post_response = client.post("/items", json={"name": "Computer Mouse", "price": 15.99})
    created_id = post_response.json()["id"]

    patch_response = client.patch(f"/items/{created_id}/restock")
    assert patch_response.status_code == 200
    assert patch_response.json()["in_stock"] is True

    patch_response_no_item = client.patch("/items/150/restock")
    assert patch_response_no_item.status_code == 404


def test_delete_item(client: TestClient):
    post_response = client.post("/items", json={"name": "Tea collection", "price": 2.99})
    created_id = post_response.json()["id"]

    delete_response = client.delete(f"/items/{created_id}")
    assert delete_response.status_code == 204

    delete_response_no_item = client.delete("/items/700")
    assert delete_response_no_item.status_code == 404
