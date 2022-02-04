from fastapi import FastAPI, Query
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'

fake_items_db = [{'item_name':'foo'}, {'item_name':'bar'},{'item_name':'Baz'}]

app = FastAPI()

@app.get('/items/')
async def read_items(q: Optional[str] = Query(None, max_length=50)):
    results = {'items': [{'item_id':'foo'}, {'item_id':'Bar'}]}
    if q:
        results.update({'q':q})
    return results

@app.post('/items_post/')
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax':price_with_tax})
    return item_dict

@app.put('/items_put/{item_id}')
async def put_item(item_id: int, item: Item, q: Optional[str]= None):
    result = {'item_id':item_id, **item.dict()}
    if q:
        result.update({'q':q})
    return result

@app.get('/items/')
async def read_item(skip: int, limit: int = 10):
    return fake_items_db[skip: skip + limit]

@app.get('/items/{item_id}')
async def read_user_item(item_id:int, needy:str):
    item = {
        'item_id':item_id,
        'needy':needy
    }
    return item

@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {'model_name': model_name, 'message': 'Deep Learning FTW!'}
    elif model_name.value == 'lenet':
        return {'model_name':model_name, 'message': 'lecnn all the images'}
    return {'model_name':model_name, 'message': 'Have some residuals'}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {'user_id': user_id}

@app.get('/files/{file_path:path}')
async def read_file(file_path: str):
    return {'file_path': file_path}