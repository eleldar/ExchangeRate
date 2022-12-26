from fastapi import FastAPI
import requests
from typing import List, Union

from pydantic import BaseModel


############Input##############

class InputData(BaseModel):
    currency: str
    count: float


############Output#############

class OutputData(BaseModel):
    sum: float


class OutputCurrencies(BaseModel):
    currencies: List[str]


##########Application##########

app = FastAPI()


@app.get('/all_currencies', response_model=OutputCurrencies, status_code=200)
async def get_all_currencies():
    rates = requests.get('https://www.cbr-xml-daily.ru/latest.js').json()['rates']
    return {'currencies': sorted(rate for rate in rates)}


@app.post('/currency', response_model=OutputData, status_code=200)
async def get_currency(request: InputData):
    rates = requests.get('https://www.cbr-xml-daily.ru/latest.js').json()['rates']
    currency = request.currency
    count = request.count
    return {'sum': round((1 / rates.get(currency)) * count, 2)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
