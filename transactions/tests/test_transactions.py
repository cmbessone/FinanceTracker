from fastapi.testclient import TestClient
from infrastructure.fastapi_app import app

client = TestClient(app)

def test_add_transaction():
    response = client.post("/transaction", json={
        "date": "10-10-2024",
        "amount": 8000,
        "category": "Ingreso",
        "description": "Salary"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Transacción agregada con éxito"}

def test_get_transactions():
    response = client.get("/transactions?start_date=10-10-2024&end_date=10-10-2024")
    assert response.status_code == 200
    transactions = response.json()
    assert len(transactions) > 0
    assert transactions[0]["amount"]==8000