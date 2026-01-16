# test_app.py
import pytest
from app import app
 
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
 
def test_home(client):
    """Test home endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello,This is a simple REST API." in response.data
 
def test_health(client):
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["service"] == "calculator-api"
 
def test_add(client):
    """Test addition endpoint"""
    response = client.get("/add?a=5&b=3")
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == 8
 
def test_add_invalid_input(client):
    """Test addition with invalid input"""
    response = client.get("/add?a=not_a_number&b=3")
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
 
def test_subtract(client):
    """Test subtraction endpoint"""
    response = client.get("/subtract?a=10&b=3")
    assert response.status_code == 200
    assert response.get_json()["result"] == 7
 
def test_multiply(client):
    """Test multiplication endpoint"""
    response = client.get("/multiply?a=4&b=5")
    assert response.status_code == 200
    assert response.get_json()["result"] == 20
 
def test_divide(client):
    """Test division endpoint"""
    response = client.get("/divide?a=20&b=4")
    assert response.status_code == 200
    assert response.get_json()["result"] == 5
 
def test_divide_by_zero(client):
    """Test division by zero"""
    response = client.get("/divide?a=10&b=0")
    assert response.status_code == 400
    data = response.get_json()
    assert "Division by zero" in data["error"]
 
def test_cube(client):
    """Test cube endpoint"""
    response = client.get("/cube?x=3")
    assert response.status_code == 200
    assert response.get_json()["result"] == 27
 
def test_greet_user(client):
    """Test greeting endpoint with name"""
    response = client.get("/greet_user/Alice")
    assert response.status_code == 200
    data = response.get_json()
    assert "Hello, Alice!" in data["message"]
 
def test_greet_optional_with_name(client):
    """Test optional greeting with name"""
    response = client.get("/greet_optional/Bob")
    assert response.status_code == 200
    data = response.get_json()
    assert "Bob" in data["message"]
 
def test_greet_optional_without_name(client):
    """Test optional greeting without name"""
    response = client.get("/greet_optional/")
    assert response.status_code == 200
    data = response.get_json()
    assert "Guest" in data["message"]
 
def test_area_post(client):
    """Test area calculation POST endpoint"""
    response = client.post("/area",
                          json={"width": 5, "height": 10},
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == 50
    assert data["units"] == "square units"
 
def test_area_missing_fields(client):
    """Test area calculation with missing fields"""
    response = client.post("/area",
                          json={"width": 5},
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
 
def test_echo_post(client):
    """Test echo endpoint"""
    test_data = {"message": "test", "numbers": [1, 2, 3]}
    response = client.post("/echo",
                          json=test_data,
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["received_data"] == test_data