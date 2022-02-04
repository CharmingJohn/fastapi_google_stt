from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id, "item_price": item.price}

@app.post("/item/")
def update_item(name: str = Form(...), price : str = Form(...)):
    return {"item_name": name, "item_price": price}

@app.post('/binary_check/')
async def binary_check(item: str = Form(...), price: float = Form(...), audio_file: UploadFile = File(...)):

    data = await audio_file.read()
    data = str(data)
    return {'name': item, 'price': price, 'data': data[:44]}