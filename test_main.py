from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_generate_qr():
    response = client.get("/generate_qr?text=Hello")
    assert response.status_code == 200
    assert "qr_code" in response.json()

def test_decode_qr():
    file_path = "tests/qr-code.png"  # Make sure you have a sample QR code for testing
    with open(file_path, "rb") as file:
        response = client.post("/decode_qr", files={"file": file})
    assert response.status_code == 200
    assert "decoded_text" in response.json()
