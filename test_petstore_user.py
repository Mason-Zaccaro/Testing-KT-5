import requests
import pytest

BASE_URL = "https://petstore.swagger.io/v2"
HEADERS = {"Content-Type": "application/json"}

@pytest.fixture  # Декоратор, превращающий функцию в фикстуру
def user_data():
    return {
          "id": 12345,
          "username": "Mason",
          "firstName": "Georgii",
          "lastName": "Zapevalov",
          "email": "Georgii@yandex.ru",
          "password": "qwerty12345",
          "phone": "117",
          "userStatus": 0
        }

def test_post_create_pet(user_data):
    response = requests.post(f"{BASE_URL}/user", json=user_data, headers=HEADERS)  # Отправляем POST-запрос для создания питомца
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"  # Проверяем, что статус код ответа равен 200
    response_data = response.json() if response.content else {}  # Преобразуем ответ в JSON
    assert response_data.get("id") == user_data["id"], "Pet ID does not match."  # Проверяем, что ID созданного питомца совпадает с ожидаемым

def test_get_pet_by_id(user_data):
    user_id = user_data["username"]  # Получаем ID юзера из фикстуры
    response = requests.get(f"{BASE_URL}/user/{user_id}")  # Отправляем GET-запрос для получения информации о питомце по его ID
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"  # Проверяем, что статус код ответа равен 200
    response_data = response.json() if response.content else {}  # Преобразуем ответ в JSON
    assert response_data.get("username") == user_data["username"], "Pet name does not match in GET request."  # Проверяем, что имя питомца в ответе совпадает с ожидаемым

def test_put_update_pet(user_data):
    updated_data = user_data.copy()  # Создаем копию данных юзера
    updated_data["name"] = "Updated_Name"  # Изменяем имя юзера
    response = requests.put(f"{BASE_URL}/user", json=updated_data, headers=HEADERS)  # Отправляем PUT-запрос для обновления информации о питомце
    assert response.status_code == 200, f"Unexpected status code: {response.status_code} for PUT request"  # Проверяем, что статус код ответа равен 200
    response_data = response.json() if response.content else {}  # Преобразуем ответ в JSON
    assert response_data.get("name") == updated_data["name"], "Pet name did not update."  # Проверяем, что имя питомца в ответе совпадает с обновленным именем

def test_delete_pet(user_data):
    user_id = user_data["id"]  # Получаем ID юзера из фикстуры
    response = requests.delete(f"{BASE_URL}/user/{user_id}")  # Отправляем DELETE-запрос для удаления питомца
    assert response.status_code == 200, f"Unexpected status code: {response.status_code} for DELETE request"  # Проверяем, что статус код ответа равен 200

    # Проверка, что юзер был удален
    response = requests.get(f"{BASE_URL}/user/{user_id}")  # Отправляем GET-запрос для проверки, что питомец был удален
    assert response.status_code == 404, f"Expected 404 for deleted pet, got {response.status_code}"  # Проверяем, что статус код ответа равен 404 (питомец не найден)