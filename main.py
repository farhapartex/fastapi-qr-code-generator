from fastapi import FastAPI, Query, File, UploadFile, HTTPException
import qrcode
from PIL import Image
from io import BytesIO
import base64
from pyzbar.pyzbar import decode

app = FastAPI()

# QR Code Generator Endpoint
@app.get("/generate_qr")
async def generate_qr(text: str = Query(..., description="Text to encode in QR code")):
    qr = qrcode.make(text)
    img_buffer = BytesIO()
    qr.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
    return {"qr_code": f"data:image/png;base64,{img_base64}"}

# QR Code Decoder Endpoint
@app.post("/decode_qr")
async def decode_qr(file: UploadFile = File(...)):
    try:
        img = Image.open(file.file)
        decoded_data = decode(img)
        if not decoded_data:
            raise HTTPException(status_code=400, detail="No QR code found in image")
        return {"decoded_text": decoded_data[0].data.decode("utf-8")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
