import requests
import pytest

BASE_URL = "https://petstore.swagger.io/v2"
HEADERS = {"Content-Type": "application/json"}

@pytest.fixture
def order_data():
    return {
        "id": 1,
        "petId": 12345,
        "quantity": 1,
        "shipDate": "2023-10-01T12:34:56.789Z",
        "status": "placed",
        "complete": True
    }

def test_post_create_order(order_data):
    response = requests.post(f"{BASE_URL}/store/order", json=order_data, headers=HEADERS)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    response_data = response.json() if response.content else {}
    assert response_data.get("id") == order_data["id"], "Order ID does not match."

def test_get_order_by_id(order_data):
    order_id = order_data["id"]
    response = requests.get(f"{BASE_URL}/store/order/{order_id}")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    response_data = response.json() if response.content else {}
    assert response_data.get("id") == order_data["id"], "Order ID does not match in GET request."

def test_delete_order(order_data):
    order_id = order_data["id"]
    response = requests.delete(f"{BASE_URL}/store/order/{order_id}")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code} for DELETE request"

    # Проверка, что заказ был удален
    response = requests.get(f"{BASE_URL}/store/order/{order_id}")
    assert response.status_code == 404, f"Expected 404 for deleted order, got {response.status_code}"

def test_get_inventory():
    response = requests.get(f"{BASE_URL}/store/inventory")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    response_data = response.json() if response.content else {}
    assert isinstance(response_data, dict), "Inventory response is not a dictionary."